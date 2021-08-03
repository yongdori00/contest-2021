import React from 'react';
import '../../App.css'
import InfoSection from '../InfoSection';
import {qnaObj} from '../InfoSection/Data';
function Home () {
    return(
        <>
        <InfoSection{...qnaObj}/>
        </>
    );
}
export default Home;