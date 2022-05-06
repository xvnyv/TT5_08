import "./App.css";
import Login from "./components/Login";
import Project from "./components/Project";
import { MainProvider } from "./context/MainContext";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import AllExpenses from "./components/AllExpenses";
import Sidebar from "./components/Sidebar";

function App() {
  return (
    <MainProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/project/*" element={<AllExpenses />} />
          <Route path="/project" element={<Sidebar />} />
        </Routes>
      </Router>
    </MainProvider>
  );
}

export default App;
