import { useState, createContext } from 'react'

const MainContext = createContext()

export const MainProvider = ({ children }) => {
  const [username,setUser] = useState('');
  const [isLogged,setIsLogged] = useState(false);
  

  return (
    <MainContext.Provider
      value={{
        username,
        isLogged,
        setUser,
        setIsLogged
      }}
    >
      {children}
    </MainContext.Provider>
  )
}

export default MainContext
