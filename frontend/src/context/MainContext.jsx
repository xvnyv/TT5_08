import { useState, createContext } from "react";

const MainContext = createContext();

export const MainProvider = ({ children }) => {
  const [username, setUser] = useState("");
  const [userID, setUserID] = useState("");
  const [appointment, setAppointment] = useState("");
  const [isLogged, setIsLogged] = useState(false);
  const [projects, setProjects] = useState([]);
  const [viewProject, setViewProject] = useState([]);
  const [token, setToken] = useState("");

  return (
    <MainContext.Provider
      value={{
        username,
        isLogged,
        setUser,
        setIsLogged,
        projects,
        setProjects,
        userID,
        setUserID,
        appointment,
        setAppointment,
        viewProject,
        setViewProject,
        token,
        setToken,
      }}
    >
      {children}
    </MainContext.Provider>
  );
};

export default MainContext;
