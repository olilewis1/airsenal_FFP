import React, { useEffect, useState } from 'react';
// import './Typewriter.css'; // Import your CSS file for styling

const Typewriter = () => {
  const [text, setText] = useState('');
  const fullText = 'hihih'; // Your desired text

  useEffect(() => {
    let currentIndex = 0;
    const interval = setInterval(() => {
      if (currentIndex <= fullText.length) {
        setText(fullText.substring(0, currentIndex));
        currentIndex++;
      } else {
        clearInterval(interval); // Stop the typing animation
      }
    }, 100); // Adjust typing speed as needed

    return () => clearInterval(interval); // Clean up the interval on unmount
  }, []);

  return (
    <div className="typewriter-container">
      <span className="typed-text">{text}</span>
    </div>
  );
};

export default Typewriter;
