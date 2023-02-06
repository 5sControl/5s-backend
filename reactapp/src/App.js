import './App.css';
import { useEffect, useState } from 'react';
import axios from "axios";

import { API_URL } from '.';

function App() {
  const [data, setData] = useState([])
  useEffect(()=>{
      axios.get(API_URL).then(data => setData(data.data.results))
  },[])
  return (
    <div className="App">
      {data.map((el) => {
        return(
        <div key={el.id}>
          <span>{el.id}</span>
          <img src={el.image} alt='image'/>
          <span>{el.action}</span>
        </div>) 
      })}
    </div>
  );
}

export default App;
