import './App.css';
import { useEffect } from 'react';
import axios from "axios";

import { API_URL } from '.';

const getStudents = (data)=>{
  axios.get(API_URL).then(data => console.log(data.data))
}



function App() {
  useEffect(()=>{
    getStudents()
  },[])
  return (
    <div className="App">
      sdfsdfsdf
    </div>
  );
}

export default App;
