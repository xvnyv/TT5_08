import React, { useRef, useContext } from "react";
import { useNavigate } from "react-router-dom";
import MainContext from "../context/MainContext";

function Login() {
  const userRef = useRef();
  const passRef = useRef();
  const axios = require("axios");
  const navigate = useNavigate();
  const { setUser, token, setProjects, setToken, setIsLogged } =
    useContext(MainContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await axios.post("http://localhost:5000/login", {
      username: userRef.current.value,
      password: passRef.current.value,
    });
    console.log(res);
    if (res.status < 300) {
      setUser(res.data.name);
      setToken(res.data.token);
      console.log(res.data.token);
      console.log(token);
      setIsLogged(true);
      navigate("/project");
    } else {
      alert("incorrect password/username!");
    }
  };

  return (
    <div className="d-flex flex-column justify-content-center">
      <h1 className="text-center">Welcome! Please log in to continue!</h1>
      <form className="loginForm" onSubmit={handleSubmit} method="POST">
        <div className="loginBox text-center mt-4">
          <div className="row justify-content-center">
            <div className="col-2">
              <label htmlFor="username" className="form-lab">
                Username
              </label>
              <input
                ref={userRef}
                type="text"
                className="form-control rounded-pill border-2"
                id="username"
                placeholder="Enter username"
              />
            </div>
          </div>
          <div className="row justify-content-center">
            <div className="col-2">
              <label htmlFor="password" className="form-lab">
                Password
              </label>
              <input
                ref={passRef}
                type="password"
                className="form-control rounded-pill border-2"
                id="password"
                placeholder="Enter password"
              />
            </div>
          </div>
          <button type="submit" className="btn btn-dark mt-3">
            Login
          </button>
        </div>
      </form>
    </div>
  );
}

export default Login;
