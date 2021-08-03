export const homeObjOne = {
    id: 'about1',
    lightBg: false,
    lightText: true,
    lightTextDesc: true,
    topLine: '한국인 사망 원인 4위, 전세계 사망 원인 2위',
    headLine: '당신은 뇌졸중으로부터 안전하다고 생각하십니까?',
    description: '뇌졸중은 혈관이 막히거나 터져서 뇌 조직이 손상되는 질환이며 국내에서는 연간 60만명에 달하는 환자들이 발생하고 있습니다. 현대인의 식습관, 흡연, 운동부족 등의 이유로 어느날 갑자기 뇌졸중이 발병할 수 있습니다. 빠른 시간 내에 대처를 하지 못한다면 반신마비, 언어장애 등 심각한 후유증으로 이어질 수 있습니다. 그래서 골든 타임인 발병 3시간 안에 병원을 찾는 것이 무엇보다 중요합니다.',
    imgStart: false,
    img: require('../../images/svg-1.svg').default,
    alt: 'doctor',
    dark: true,
    primary: true,
    darkText: false
}

export const homeObjTwo = {
    id: 'about2',
    lightBg: true,
    lightText: false,
    lightTextDesc: false,
    topLine: '머신 러닝과 빅 데이터를 활용한',
    headLine: '뇌졸중 초기 진단 프로그램 "건강한 얼굴 건강한 정신"',
    description: '뇌졸중의 초기 증상 중 하나인 안면 마비는 전문적 지식이 없는 일반인들도 환자의 상태를 파악하는데 큰 도움이 됩니다. 하지만 뇌졸중이 발병한 환자들은 거울을 보고 스스로 안면 마비 증세가 나타나고 있음을 인지하지 못하는 경우가 많기 때문에 1인 가구 또는 홀로 생활하는 사람들은 초기에 알아차리기가 어렵습니다. 그리하여 혼자서도 카메라 하나로 안면 마비 증세를 인지할 수 있는 프로그램을 개발하게 되었습니다.',
    imgStart: true,
    img: require('../../images/svg-2.svg').default,
    alt: 'tech',
    dark: false,
    primary: false,
    darkText: true
}

export const homeObjThree = {
    id: 'about3',
    lightBg: false,
    lightText: true,
    lightTextDesc: true,
    topLine: 'dlib, OpenCV, Python을 활용한',
    headLine: '얼굴 주요 부위를 탐색하는 Facial Landmark Detection 알고리즘',
    description: '뇌졸중 환자의 안면 마비 증상은 일반적으로 한쪽으로 쳐진 입술, 눈, 눈썹 등과 같은 특징과 전체적으로 비대칭성을 보이는 얼굴에서 나타납니다. 저희 팀은 그러한 특징들에 착안하여 눈, 코, 입, 턱과 같은 얼굴의 주요 부위들을 인식하여 점의 좌표로 나타내는 Facial Landmark Detection 알고리즘을 활용하였습니다.',
    imgStart: false,
    img: require('../../images/img-5.jpg').default,
    alt: 'face-recognition',
    dark: true,
    primary: true,
    darkText: false
}

export const homeObjFour = {
    id: 'about4',
    lightBg: true,
    lightText: false,
    lightTextDesc: false,
    topLine: '뇌졸중과 안면 마비에 관련된 논문을 참고하여 작성한',
    headLine: '"건강한 얼굴 건강한 정신"의 마비 증상 계산 방법',
    description: '얼굴의 비대칭성 특징에 집중하여 총 세 가지 길이를 사용해 계산 했습니다. 코의 중앙에서 시작하여 입술 양쪽 끝까지의 길이, 코의 양쪽 끝까지의 길이 그리고 눈 양쪽 끝까지의 길이를 각각 구하여 둘 중 큰 값을 작은 값으로 나누었습니다. 그리고 각 값을 모두 더하였는데 안면 마비 증상이 없는 정상인의 경우에는 이 값이 3에 가깝게 나오게 되고 뇌졸중으로 인한 안면 마비 증상을 경험하고 있는 사람은 값이 더 크게 나오게 됩니다.',
    imgStart: true,
    img: require('../../images/img-7.jpg').default,
    alt: 'tech',
    dark: false,
    primary: false,
    darkText: true
}

export const homeObjFive = {
    id: 'about5',
    lightBg: false,
    lightText: true,
    lightTextDesc: true,
    topLine: '학습 알고리즘을 통한 머신 러닝 과정',
    headLine: '학습 알고리즘을 통한 머신 러닝 과정',
    description: '인터넷상에서 구한 뇌졸중으로 인한 안면 마비 증상을 보이고 있는 환자들의 얼굴 사진과 그렇지 않은 정상인 얼굴 사진을 총 1000장 가까이 사용하여, 프로그램한테 임의의 사진이 주어졌을 때 안면 마비 증상의 여부를 판단할 수 있도록 학습 하였습니다.',
    imgStart: false,
    img: require('../../images/svg-4.svg').default,
    alt: 'face-recognition',
    dark: true,
    primary: true,
    darkText: false
}

export const qnaObj = {
    id: 'qna',
    lightBg: false,
    lightText: true,
    lightTextDesc: true,
    topLine: '언제든지 연락 주세요!',
    headLine: '이름 @이메일',
    description: '프로그램에 대해 궁금한 사항이나 개선 방안이 있으시면 언제든지 연락 바랍니다',
    img: require('../../images/svg-3.svg').default,
    alt: 'developer',
    dark: true,
    primary: true,
    darkText: false
}