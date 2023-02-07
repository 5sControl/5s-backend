import React from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";

import './index.scss';
import Report from './pages/report/Report';
import { RoutesOutlet } from './routes/Routes';

function App() {
    return (
      <BrowserRouter>
      <Routes>
            <Route element={<RoutesOutlet/>}>
                <Route
                    path="/"
                    element={<Report/>}
                />
            </Route>
        </Routes>
       </BrowserRouter>
    );
  }
  
  export default App;