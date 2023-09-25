import {useEffect, useState} from 'react'
import axios from 'axios';
const DataFPL = () => {

  const [playerDataState, setPlayerDataState] = useState({  });   
  const apiHost = 'api-football-v1.p.rapidapi.com';
  const apiKey = '11964f2e97msh056f5a816e1157ep13ab3djsn6b0dbc5fe3aa';

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          `https://api-football-v1.p.rapidapi.com/v3/players?league=39&season=2023&page=1`,
          {
            params: {
              league: 39,
              season: 2023,
            },
            headers: {
              'X-RapidAPI-Host': apiHost,
              'X-RapidAPI-Key': apiKey,
            },
          }
        );
        console.log(response.data)
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchData();
   
  
  }, [playerDataState]);
  
  return (
    <div>DataFPL</div>
  )
}

export default DataFPL