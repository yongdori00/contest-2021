import cv2
import dlib
import numpy
import math
import sys
import glob
import base64
import os
from skimage import io
from PIL import Image
from django.conf import settings

CAM_ID = 0

PREDICTOR_PATH = settings.STATIC_ROOT_URL + settings.STATIC_URL + "data/shape_predictor_68_face_landmarks.dat"
SCALE_FACTOR = 1 
FEATHER_AMOUNT = 11

LEFT_LIP = 0
RIGHT_LIP = 0
LEFT_EYE = 0
RIGHT_EYE = 0

FACE_POINTS = list(range(17, 68))
MOUTH_POINTS = list(range(48, 61))
RIGHT_BROW_POINTS = list(range(17, 22))
LEFT_BROW_POINTS = list(range(22, 27))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
NOSE_POINTS = list(range(27, 35))
JAW_POINTS = list(range(0, 17))

# Points used to line up the images.
ALIGN_POINTS = (LEFT_BROW_POINTS + RIGHT_EYE_POINTS + LEFT_EYE_POINTS +
                               RIGHT_BROW_POINTS + NOSE_POINTS + MOUTH_POINTS)

# Points from the second image to overlay on the first. The convex hull of each
# element will be overlaid.
OVERLAY_POINTS = [
    LEFT_EYE_POINTS + RIGHT_EYE_POINTS + LEFT_BROW_POINTS + RIGHT_BROW_POINTS,
    NOSE_POINTS + MOUTH_POINTS,
]

# Amount of blur to use during colour correction, as a fraction of the
# pupillary distance.
COLOUR_CORRECT_BLUR_FRAC = 0.6

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

f = open(settings.STATIC_ROOT_URL + settings.STATIC_URL + "/data/data.txt", 'r')
W = numpy.array(float(f.readline().rstrip('\n')))
W = numpy.array(W).reshape(1,1)
b = numpy.array(float(f.readline()))
b = numpy.array(b).reshape(1)
    
def newSection():
    def terminal_size():
        import fcntl, termios, struct
        h, w, hp, wp = struct.unpack('HHHH',
            fcntl.ioctl(0, termios.TIOCGWINSZ,
            struct.pack('HHHH', 0, 0, 0, 0)))
        return w
    ter_int = terminal_size()
    print ("\n" + ("_" * (int(ter_int))) + "\n\n")


def sigmoid(x):
    return 1/(1+numpy.exp(-x))
    
def predict(x):
    z = numpy.dot(x, W) + b
    y = sigmoid(z)
    
    if y > 0.5:
        result = 1
    else:
        result = 0
        
    return y, result

def dist(x, y):
    a = x[0,0] - y[0,0]
    b = x[0,1] - y[0,1]
    return math.sqrt((a*a) + (b*b))

class TooManyFaces(Exception):
    pass

class NoFaces(Exception):
    pass

def get_landmarks(im):
    rects = detector(im, 1)
    
    if len(rects) > 1:
        #raise TooManyFaces
        return None
    if len(rects) == 0:
        #raise NoFaces
        return None
    else:
        return numpy.matrix([[p.x, p.y] for p in predictor(im, rects[0]).parts()])

def annotate_landmarks(im, landmarks):
    im = im.copy()
    for idx, point in enumerate(landmarks):
        pos = (point[0, 0], point[0, 1])
        cv2.putText(im, str(idx), pos,
                    fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    fontScale=0.4,
                    color=(0, 0, 255))
        cv2.circle(im, pos, 3, color=(0, 255, 255))
    return im

def draw_convex_hull(im, points, color):
    points = cv2.convexHull(points)
    cv2.fillConvexPoly(im, points, color=color)

def get_face_mask(im, landmarks):
    im = numpy.zeros(im.shape[:2], dtype=numpy.float64)

    for group in OVERLAY_POINTS:
        draw_convex_hull(im,landmarks[group],color=1)

    im = numpy.array([im, im, im]).transpose((1, 2, 0))

    im = (cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0) > 0) * 1.0
    im = cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0)

    return im
    
def transformation_from_points(points1, points2):
    """
    Return an affine transformation [s * R | T] such that:
        sum ||s*R*p1,i + T - p2,i||^2
    is minimized.
    """
    # Solve the procrustes problem by subtracting centroids, scaling by the
    # standard deviation, and then using the SVD to calculate the rotation. See
    # the following for more details:
    #   https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem

    points1 = points1.astype(numpy.float64)
    points2 = points2.astype(numpy.float64)

    c1 = numpy.mean(points1, axis=0)
    c2 = numpy.mean(points2, axis=0)
    points1 -= c1
    points2 -= c2

    s1 = numpy.std(points1)
    s2 = numpy.std(points2)
    points1 /= s1
    points2 /= s2

    U, S, Vt = numpy.linalg.svd(points1.T * points2)

    # The R we seek is in fact the transpose of the one given by U * Vt. This
    # is because the above formulation assumes the matrix goes on the right
    # (with row vectors) where as our solution requires the matrix to be on the
    # left (with column vectors).
    R = (U * Vt).T

    return numpy.vstack([numpy.hstack(((s2 / s1) * R,
                                       c2.T - (s2 / s1) * R * c1.T)),
                         numpy.matrix([0., 0., 1.])])
    
    
def read_im_and_landmarks(fname):
    im = cv2.imread(fname, cv2.IMREAD_COLOR)
    im = cv2.resize(im, (im.shape[1] * SCALE_FACTOR, im.shape[0] * SCALE_FACTOR))
    s = get_landmarks(im)
    if s is None:
        print('Face Error')
        return 999
    else:
        CENTER = s[33]
        LEFT_LIP = s[48]
        RIGHT_LIP = s[54]
        LEFT_EYE = s[36]
        RIGHT_EYE = s[45]
        LEFT_NOSE = s[31]
        RIGHT_NOSE = s[35]
        left_eye = dist(CENTER, LEFT_EYE)
        right_eye = dist(CENTER, RIGHT_EYE)
        left_lip = dist(CENTER, LEFT_LIP)
        right_lip = dist(CENTER, RIGHT_LIP)
        left_nose = dist(CENTER, LEFT_NOSE)
        right_nose = dist(CENTER, RIGHT_NOSE)

        eye_rate = 0
        lip_rate = 0
        nose_rate = 0

        ret = 0
        if(left_eye > right_eye):
            ret += (right_eye/left_eye)
            eye_rate = (right_eye/left_eye)
        else:
            ret += (left_eye/right_eye)
            eye_rate = (left_eye/right_eye)
        if(left_lip > right_lip):
            ret += (right_lip/left_lip)
            lip_rate = (right_lip/left_lip)
        else:
            ret += (left_lip/right_lip)
            lip_rate = (left_lip/right_lip)
        if(left_nose > right_nose):
            ret += (right_nose/left_nose)
            nose_rate = (right_nose/left_nose)
        else:
            ret += (left_nose/right_nose)
            nose_rate = (left_nose/right_nose)
        print(3 - ret)
    print(lip_rate)
    return im, s, eye_rate, lip_rate, nose_rate

def left_right_gap(fname):
    im = cv2.imread(fname, cv2.IMREAD_COLOR)
    im = cv2.resize(im, (im.shape[1] * SCALE_FACTOR, im.shape[0] * SCALE_FACTOR))
    s = get_landmarks(im)
    if s is None:
        return 999
    else:
        CENTER = s[33]
        LEFT_LIP = s[48]
        RIGHT_LIP = s[54]
        LEFT_EYE = s[36]
        RIGHT_EYE = s[45]
        LEFT_NOSE = s[31]
        RIGHT_NOSE = s[35]
        left_eye = dist(CENTER, LEFT_EYE)
        right_eye = dist(CENTER, RIGHT_EYE)
        left_lip = dist(CENTER, LEFT_LIP)
        right_lip = dist(CENTER, RIGHT_LIP)
        left_nose = dist(CENTER, LEFT_NOSE)
        right_nose = dist(CENTER, RIGHT_NOSE)

        ret = 0
        if(left_eye > right_eye):
            ret += (right_eye/left_eye)
        else:
            ret += (left_eye/right_eye)
        if(left_lip > right_lip):
            ret += (right_lip/left_lip)
        else:
            ret += (left_lip/right_lip)
        if(left_nose > right_nose):
            ret += (right_nose/left_nose)
        else:
            ret += (left_nose/right_nose)
        return (3 - ret)

def warp_im(im, M, dshape):
    output_im = numpy.zeros(dshape, dtype=im.dtype)
    cv2.warpAffine(im,
                   M[:2],
                   (dshape[1], dshape[0]),
                   dst=output_im,
                   borderMode=cv2.BORDER_TRANSPARENT,
                   flags=cv2.WARP_INVERSE_MAP)
    return output_im

def correct_colours(im1, im2, landmarks1):
    blur_amount = COLOUR_CORRECT_BLUR_FRAC * numpy.linalg.norm(
                              numpy.mean(landmarks1[LEFT_EYE_POINTS], axis=0) -
                              numpy.mean(landmarks1[RIGHT_EYE_POINTS], axis=0))
    blur_amount = int(blur_amount)
    if blur_amount % 2 == 0:
        blur_amount += 1
    im1_blur = cv2.GaussianBlur(im1, (blur_amount, blur_amount), 0)
    im2_blur = cv2.GaussianBlur(im2, (blur_amount, blur_amount), 0)

    # Avoid divide-by-zero errors.
    im2_blur += (128 * (im2_blur <= 1.0)).astype(im2_blur.dtype)

    return (im2.astype(numpy.float64) * im1_blur.astype(numpy.float64) /
                                                im2_blur.astype(numpy.float64))
    
def use_image(FilePath): #있는 이미지 사용
    im1, landmarks1 = read_im_and_landmarks(FilePath)
    mask = get_face_mask(im1, landmarks1)
    # Run the HOG face detector on the image data
    detected_faces = detector(im1, 1)
    root, extension = os.path.splitext(FilePath)
    
    if extension == '.png' or '.PNG':
        img = Image.open(FilePath).convert('RGB')
        name = root + '.jpg'
        img.save(name, 'jpeg')
        os.remove(root + '.png')
    win = dlib.image_window()
    image = io.imread(root+'.jpg')
    cv2.imwrite('test2.jpg',image)    
    # Show the desktop window with the image
    win.set_image(image)
    for i, face_rect in enumerate(detected_faces):
        # Detected faces are returned as an object with the coordinates 
        # Draw a box around each face we found
        win.add_overlay(face_rect)
        # Get the the face's pose
        pose_landmarks = predictor(image, face_rect)
        win.add_overlay(pose_landmarks)
        #cv2.imshow('frame', image)
        cv2.imwrite('test.jpg', image)
        # facial landmark represent red point
    
        for j in range(68):
            x = pose_landmarks.part(j).x
            y = pose_landmarks.part(j).y
            cv2.circle(im1, (x,y), 1, (0, 0, 255), -1)
        cv2.rectangle(im1,(face_rect.left(),face_rect.top()),
                  (face_rect.right(),face_rect.bottom()),
                   (0,255,0),2)
        crop = im1[face_rect.top():face_rect.bottom(),face_rect.left():face_rect.right()]
        cv2.imwrite(FilePath[:-4] + '_new.jpg',crop)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        os.remove(root+'.jpg')
        # Draw the face landmarks on the screen. 
    pre_num = predict(left_right_gap(root + '_new.jpg'))[0][0][0]
    
    if pre_num >= 0.5:
        return True, crop
    else:
        return False, crop


def use_string(FilePath, base_64_img):
    
    with open(settings.MEDIA_ROOT_URL + settings.MEDIA_URL + "str_img.webp", "wb") as fh:
        fh.write(base64.b64decode(base_64_img))
    fh.close()
    
    temp = Image.open(settings.MEDIA_ROOT_URL + settings.MEDIA_URL + "str_img.webp").convert("RGB")
    temp.save(settings.MEDIA_ROOT_URL + settings.MEDIA_URL + "str_img.jpg", "jpeg")
    
    argv = settings.MEDIA_ROOT_URL + settings.MEDIA_URL + "str_img.jpg"
    im1, landmarks1, eye_rate, lip_rate, nose_rate = read_im_and_landmarks(argv)
    mask = get_face_mask(im1, landmarks1)
    # Run the HOG face detector on the image data
    detected_faces = detector(im1, 1)
    root, extension = os.path.splitext(argv)
    
    #win = dlib.image_window()
    image = io.imread(root+'.jpg')
    #image = io.imread(argv,plugin='matplotlib')
    #image.imread(argv,pilmode="RGB")

    cv2.imwrite('test2.jpg',image)    

    # Show the desktop window with the image
    #win.set_image(image)
    for i, face_rect in enumerate(detected_faces):
        # Detected faces are returned as an object with the coordinates 
        # Draw a box around each face we found
        #win.add_overlay(face_rect)
        # Get the the face's pose
        pose_landmarks = predictor(image, face_rect)
        #win.add_overlay(pose_landmarks)
        #cv2.imshow('frame', image)
        cv2.imwrite('test.jpg', image)
        # facial landmark represent red point
    
        for j in range(68):
            x = pose_landmarks.part(j).x
            y = pose_landmarks.part(j).y
            cv2.circle(im1, (x,y), 1, (0, 0, 255), -1)
        cv2.rectangle(im1,(face_rect.left(),face_rect.top()),
                  (face_rect.right(),face_rect.bottom()),
                   (0,255,0),2)
        crop = im1[face_rect.top():face_rect.bottom(),face_rect.left():face_rect.right()]
        cv2.imwrite(FilePath,crop)
        # Draw the face landmarks on the screen. 
    pre_num = predict(left_right_gap(FilePath))[0][0][0]

    with open(FilePath, 'rb') as img:
        cropped_img = base64.b64encode(img.read()).decode('utf8')
        
    if pre_num >= 0.5:
        return True, cropped_img, eye_rate, lip_rate, nose_rate
    else:
        return False, cropped_img, eye_rate, lip_rate, nose_rate


def result_main(base_64_img, is_string, Filepath):
    is_stroke = True
    if is_string == True:
        is_stroke, cropped_img, eye_rate, lip_rate, nose_rate = use_string(Filepath, base_64_img)
        return is_stroke, cropped_img, eye_rate, lip_rate, nose_rate
        #return is_stroke, cropped_img, LEFT_EYE[0][0], LEFT_LIP[0][0], RIGHT_EYE[0][0], RIGHT_LIP[0][0], LEFT_EYE[0][1], LEFT_LIP[0][1], RIGHT_EYE[0][1], RIGHT_LIP[0][1]
    elif is_string == False:
        is_stroke, cropped_img = use_image(base_64_img)
        return is_stroke, cropped_img