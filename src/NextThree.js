import React from 'react'

const NextThree = (props) => {
  console.log(props )
  function hi(propsToUse) {
    const mapping_position = ['GK', 'DEF', 'MID', 'FWD'];
    
    mapping_position.forEach(position => {
      console.log(position + ':');
      propsToUse[position].forEach(player => {
        console.log(player);
      });
    });
  }
  
  // Call the hi function with your props object
  hi(props);
  
  const mapping_position = ['GK', 'DEF', 'MID', 'FWD']
  return (
    <div>
      {mapping_position.map((position) => (
        <div className={'test'}key={position}>
          {position + ':'}
          {props[position].map((player, index) => (
            <>
            <div key={index}>{player.name}</div>
            <div key={index}>{player.price}</div>
            <div key={index}>{player.club}</div>
            <div key={index}>{player.points}</div>
            </>
          ))}
        </div>
      ))}
    </div>
  );
};

export default NextThree