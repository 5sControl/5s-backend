import './App.css';
import { useEffect, useState } from 'react';
import axios from "axios";

import { API_URL } from '.';

function App() {
  const [data, setData] = useState([])
  useEffect(()=>{
      axios.get(API_URL).then(data => {
        setData(data.data.results)
        console.log(data.data.results)
      })
      
  },[])
  return (
    <div className="App">
      <section className='wrapper'>
        <ul className='control_type'>
          <li className=''>Safety control</li>
          <li className='non-active'>Idle control</li>
          <li className='non-active'>Operation control</li>
          <li className='non-active'>Staff control</li>
          <li className='non-active'>Tool control</li>
        </ul>
        <ul className='control_date'>
          <li>Today</li>
          <li>Yesterday</li>
          <li>04.02.2023</li>
        </ul>
        <div className='control_reports'>
          {data.map((el) => {
              return(
              <div key={el.id}>
                <span>{el.id}</span>
                  {el.image!=='link' && <img src={require(`./${el.image}`)} alt='image'/>}
                <span>{el.action}</span>
              </div>) 
            })}
        </div>
      </section>

    </div>
  );
}

export default App;
