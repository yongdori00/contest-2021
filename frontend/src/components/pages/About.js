import React from 'react';
import '../../App.css'
import InfoSection from '../InfoSection';
import { homeObjFive, homeObjFour, homeObjOne, homeObjThree, homeObjTwo } from '../InfoSection/Data';
function Home () {
    return(
        <>
        <InfoSection{...homeObjOne}/>
        <InfoSection{...homeObjTwo}/>
        <InfoSection{...homeObjThree}/>
        <InfoSection{...homeObjFour}/>
        <InfoSection{...homeObjFive}/>
        </>
    );
}
export default Home;