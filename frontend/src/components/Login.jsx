import React,{useRef} from 'react'

function Login() {
    const userRef = useRef();
    const passRef = useRef();

    

  return (
    <div>
        <form className="loginForm" method='POST'>
            <div className='loginBox text-center mt-4'>
                <div className='row justify-content-center'>
                    <div className='col-6'>
                        <label htmlFor="username" className="form-lab">Username</label>
                        <input ref={userRef} type="text" className="form-control rounded-pill border-2" id='username' placeholder='Enter username' />
                    </div>
                </div>
                <div className='row justify-content-center'>
                    <div className="col-6">
                        <label htmlFor="password" className="form-lab">Password</label>
                        <input ref={passRef} type="password" className="form-control rounded-pill border-2" id='password' placeholder='Enter password' />
                    </div>
                </div>
                <button type="submit" className="btn btn-primary mt-3">Login</button>
            </div>
        </form>
    </div>
  )
}

export default Login