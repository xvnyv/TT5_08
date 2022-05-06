
import './App.css';
import Login from './components/Login'
import { MainProvider } from './context/MainContext';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

function App() {
  return (
    <MainProvider>
      <Router>
        <Routes>
          <Route path='/' element={
            <Login />
          } />
          
          
        </Routes>

      </Router>
    </MainProvider>
  );
}

export default App;
