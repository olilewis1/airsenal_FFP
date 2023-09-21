import React, { useEffect, useState, useRef } from 'react';
import playerData from './data/player_data_next_three.json';
import NextThree from './NextThree';
import './App.css';

function App() {
  // Define the playerData state
  const [playerDataState, setPlayerDataState] = useState({ playerData });   


  // Define the input state
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('')
  const inputRef = useRef()
  const [outPutCheck, setOutputCheck] = useState(0)
  const outPutArray = ['$ Input Login Email', '$ Input FPL Password', '$ Input FPL ID']
  useEffect(() => {
    inputRef.current.focus()
  }, [])
  return (
    <div className='App' 
    onClick={e=> {   inputRef.current.focus()}}>
      {/* <NextThree {...playerDataState.playerData}/> */}
      {/* Input field */}
      
   

      {/* Display the current 'input' state */}
      <div className='terminal'>{output}</div>
      <div>{outPutArray[outPutCheck]}</div>
      <input
      ref={inputRef}
        type='text'
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={e => { 
          if (e.key === 'Enter') { 
            let newOutput = '' 
            newOutput = output + '\n' + '$ ' + input + '\n'
            if( input.includes('@') ) { 
              newOutput += 'Email'
              const newOutputCheck = outPutCheck + 1 
              setOutputCheck(newOutputCheck) 
            } else if (input === 'login') { 
              newOutput += 'Login received'
            } 
            else { 
              newOutput += 'Login Details Not Found'
            }
            setOutput(newOutput)
            setInput('')
          } 
        }}
      />
    </div>
  );
}

export default App;
