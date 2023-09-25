import React, { useState, useEffect } from 'react';
import fff from './assets/FFF_logo.jpeg'
import playerNextThree from './data/next_three_data.json'
import NextThree from './NextThree';
import './App.css';
import Typewriter from 'typewriter-effect';
import { useTypewriter } from 'react-simple-typewriter'
import TypewriterAI from './Typerwriter.js';
function App() {
  const [text] = useTypewriter({
    words: ['Hello'],
    loop: false
  })

  // Define the playerData state

  return (
    <div className='App text-center ' 
    >
 <TypewriterAI />
      <div className='img_fff   d-flex justify-content-center flex-column align-items-center '> <div className='w-50 mt-3 '> <img src={fff} alt="fff"  className='img-fluid img-thumbnail'/></div> <div> <h1 className='text-center mt-3'>Fantasy Football Friend </h1></div>       <div> Data led, football first.</div> </div>
      <div className='d-flex justify-content-center mt-3'>
      <div className=' terminal w-100'>
      <div className= 'd-flex justify-content-center align-items-center'>  <div className='small mt-3 w-75'>  <Typewriter
  options={{
    strings: ['hihih'],
    autoStart: true,
    loop: false,
    deleteSpeed: 0, // Set deleteSpeed to 0

  }}
/>

      <div className='mt-3'> Paired with the Alan Turing Institue, bringing a machine learning AI experience to FPL. Enabling users to: Predict the top scorers for the next 3 gameweeks Transfer and chip suggestions Recommendations for your starting 11 and subs. App incoming with all the data driven FPL you could ever need.</div>
      </div>
      </div> </div>
      {/* <NextThree {...playerDataState.playerData} /> */}
      </div>


      <div className='d-flex justify-content-center'> 
      <div className='w-50  mt-3'>Enter your Details. Let us do the rest.</div>
      </div>
      <div className='d-flex mt-3 justify-content-center align-items-center '> 
      <form className='w-75'>
  <div class="form-group">
    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
  </div>
  <div class="form-group">
    <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password" />
  </div>
  <div class="form-group">
    <input type="text" class="form-control" id="fplId" placeholder="FPL ID" />
  </div>
  <button type="submit" class="btn btn-primary btn-fff mt-3">Submit</button>
</form>
      </div>

    </div>
  );
}

export default App;
