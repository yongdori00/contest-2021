import React, {useState} from 'react';
import styled from 'styled-components';
import {MdClose} from 'react-icons/md';
import { Button } from './Button';
import axios from 'axios';
import { ResultModal } from './ResultModal';
import xtype from 'xtypejs';
import Webcam from "react-webcam";

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
    display: flex;
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
export const ImagePreview = ({showImagePreview, setShowImagePreview}) => {
    //const [image, setImage] = useState('');
    const [showResultModal, setShowResultModal] = useState(false);
    var ip = null;
    const webcamRef = React.useRef(null);

    const capture = React.useCallback(
        () => {
        const imageSrc = webcamRef.current.getScreenshot();
        console.log(imageSrc)
        const URL = "http://localhost:8000/api/";
        
        axios.post(URL, {
            'description' : ip,
            'document' : imageSrc
        })
        .then((Response)=>{console.log(Response.data)})
        .catch((Error)=>{console.log(Error)})
        setShowImagePreview(prev=>!prev);
        setShowResultModal(prev=>!prev);
        },
        [webcamRef] 
        
    ); 
    
    const getData = async () => {
        const res = await axios.get('https://geolocation-db.com/json/');
        console.log(res.data);
        ip = res.data.IPv4;
    }
    getData();

    const videoConstraints = {
        width: 1280,
        height: 720,
        facingMode: "user"
    };
    return(
        <>
        <ResultModal showResultModal={showResultModal} setShowResultModal={setShowResultModal}/>
        {showImagePreview ? (
            <Background>
                
                <ModalWrapper showImagePreview={showImagePreview}>
                
                <Webcam
                            audio={false}
                            height={720}
                            ref={webcamRef}
                            //screenshotFormat="image/jpeg"
                            width={1280}
                            mirrored={false}
                            imageSmoothing={true}
                            //forceScreenshotSourceSize="true"
                            videoConstraints={videoConstraints}
                            style={{
                                height: "100%",
                                width: "100%",
                                objectFit: "scale-down",
                                position: "absolute"
                            }}
                        />
                <button>
                <Button className="btns" buttonStyle='btn--primary' buttonSize='btn--outline' onClick={capture}>캡쳐<i className="fas fa-paper-plane"></i></Button>

                </button>
                <CloseModalButton onClick={()=>setShowImagePreview(prev=>!prev)}/>
                </ModalWrapper>
                
            </Background>
            ): null}
        </>
    )
}