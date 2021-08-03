import React, {useState} from 'react';
import styled from 'styled-components';
import {MdClose} from 'react-icons/md';
import Webcam from "react-webcam";
import { Button } from './Button';
import { ImagePreview } from './ImagePreview';
const Background = styled.div`
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    //position: fixed;
    display: flex;
    justify-content: center;
    align-items: center;
`

const ModalWrapper = styled.div`
    width: 1000px;
    height: 750px;
    box-shadow: 0 5px 16px rgba(0,0,0,0.2);
    background: #fff;
    color: #000;
    display: grid;
    grid-template-columns: 1fr 1fr;
    position: absolute;
    z-index: 10;
    border-radius: 10px;
`
const ModalVid = styled.div`
    width: 100%;
    height: 100%;
    border-radius: 10px 0 0 10px;
    background: #000;
`
const ModalImg = styled.img`
    width: 100%;
    height: 100%;
    border-radius: 10px 0 0 10px;
    background: #000;
`

const ModalContent = styled.div`
    display: flex;
    flex-direction: column;
    //justify-content: center;
    //align-items: center;
    margin-left: 10px;
    line-height: 1.8;
    color: #141414;

    p{
        margin-bottom: 1rem;
    }

    button{
        padding: 10px 24px;
        background: #141414;
        color: #fff;
        border: none;
    }
`

const CloseModalButton = styled(MdClose)`
    cursor: pointer;
    position: absolute;
    top: 20px;
    right: 20px;
    width: 32px;
    height: 32px;
    padding: 0;
    z-index: 10;
`

export const Modal = ({showModal, setShowModal}) =>{
    const [image, setImage] = useState('');
    const [showImagePreview, setShowImagePreview] = useState(false);

    const webcamRef = React.useRef(null);

    const capture = React.useCallback(
        () => {
        const imageSrc = webcamRef.current.getScreenshot();
        setImage(imageSrc);
        setShowImagePreview(prev => !prev);
        setShowModal(prev => !prev);
        },
        [webcamRef] 
        
    ); 
    const videoConstraints = {
        width: 1280,
        height: 720,
        facingMode: "user"
    };
    return(
        <>
            <ImagePreview showImagePreview={showImagePreview} setShowImagePreview={setShowImagePreview} ImageSrc={image}/>
            {showModal ? (
            <Background>
                
                <ModalWrapper showModal={showModal}>
                        <Webcam
                            audio={false}
                            //height={720}
                            ref={webcamRef}
                            screenshotFormat="image/jpeg"
                            //width={1280}
                            mirrored={false}
                            imageSmoothing={true}
                            forceScreenshotSourceSize="true"
                            videoConstraints={videoConstraints}
                            style={{
                                height: "100%",
                                width: "100%",
                                objectFit: "scale-down",
                                position: "absolute"
                            }}
                        />
                    
                    
                
                <CloseModalButton onClick={()=>setShowModal(prev=>!prev)}/>
                <button>
                <ModalContent>
                        <h1>검사 방법</h1>
                        <p>웹 카메라가 준비되어 있는지 확인 해주세요</p>
                        <p>1. 얼굴에 그림자가 지지 않도록 밝은 곳에서 진행 해주세요</p>
                        <p>2. 정면을 보고 웃어주세요</p>
                        <p>3. 카메라를 응시한 채 '사진 찍기' 버튼을 눌러주세요</p>
                        <p>4. 사진이 제대로 나왔는지 확인 후 '제출' 버튼을 통해 제출 해주세요</p>
                        <p>5. 결과가 나올 때 까지 잠시 기다려주세요</p>
                    </ModalContent>
                <Button className="btns" buttonStyle='btn--outline' buttonSize='btn--large' onClick={capture}>사진 찍기<i className="fas fa-camera"></i></Button>
                </button>
                </ModalWrapper>
            </Background>
            ): null}
        </>
    )
}