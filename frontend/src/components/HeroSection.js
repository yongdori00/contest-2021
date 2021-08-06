import React, {useState} from 'react';
import '../App.css';
import {Button} from './Button';
import './HeroSection.css';
import backgroundVideo from '../videos/video-7.mp4';

import { Modal } from './Modal';
import { GlobalStyle } from './globalStyle';

function HeroSection() {
    
    const [showModal, setShowModal] = useState(false);
    const openModal = () => {
        setShowModal(prev => !prev)
    }
    //<Button className="btns" buttonStyle='btn--outline' buttonSize='btn--large'>사진 업로드<i className="fas fa-images"></i></Button>
    return (
        <div className='hero-container'>
            <video src={backgroundVideo} autoPlay loop muted id='video'/>
            <h1>뇌졸중 초기 진단 프로그램</h1>
            <p>지금 받아보세요</p>
            <div className="hero-btns">
                <Button className="btns" buttonStyle='btn--outline' buttonSize='btn--large' onClick={openModal}>사진 찍기<i className="fas fa-camera"></i></Button>
                <Modal showModal={showModal} setShowModal={setShowModal}/> 
                
                <GlobalStyle/>
            </div>
            
        </div>
    )
}

export default HeroSection
