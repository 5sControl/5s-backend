import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

export const API_URL = "http://0.0.0.0:8080/api/safety/action/"
export const API_STATIC_MEDIA = "http://0.0.0.0:8000/static/"

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);