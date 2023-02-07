import './Dashboard.scss';
import { Fragment, useEffect, useState } from 'react';
import axios from "axios";

import { API_URL, API_IMAGES } from '../../api/api.js';

function Dashboard() {
  const [data, setData] = useState([])
  useEffect(()=>{
      axios.get(API_URL).then(data => {
        setData(data.data.results)
        console.log(data.data.results)
      })
      
  },[])
  return (
    
    <div className='dashboard'>

    </div>
  );
}

export default Dashboard;
