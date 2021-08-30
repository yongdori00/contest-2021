import React, {useState} from 'react';
import styled from 'styled-components';
import {MdClose} from 'react-icons/md';
import axios from 'axios';
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

export const ResultModal = ({showResultModal, setShowResultModal}) =>{
    const [ready, setReady] = useState(false);
    let [results, setResults] = useState([]);
    const getResult = () => {
        const URL = "http://localhost:8000/";
        axios.get(URL)
        .then((Response)=>{console.log(Response.data)})
        .catch((Error)=>{console.log(Error)})
        //const obj = JSON.parse(Response.data);
        //console.log(obj.result);
    }
    getResult();
    return(
        <>
            
            {showResultModal ? (
            <Background>
                <ModalWrapper showResultModal={showResultModal}>
                {ready ? null: (<p>Loading</p>)}        
                <CloseModalButton onClick={()=>setShowResultModal(prev=>!prev)}/>
                
                </ModalWrapper>
            </Background>
            ): null}
        </>
    )
}