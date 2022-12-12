import React, { useEffect, useState } from 'react';
import { getTokenFromResponse, loginUrl } from "./Spotify";
import slogo from "./images/spotify.jpg"

function Login(props) {
    const [token, setToken] = useState(null);
    let hash = window.location.hash;

    console.log("In Login...");

    useEffect(() => {
        console.log("Useeffect was called....");
        hash = window.location.hash;
        console.log("Windows hash " + hash);
        console.log("token is now " + token);

        if (hash !== null) {
            const newToken = getTokenFromResponse(hash).access_token;
            setToken(newToken);
            props.onAuthorisationComplete(newToken);
            console.log("TOken " + newToken);
        }
    }, [hash, token, props]);

    return (
        <div className="login">
            <img
                src={slogo}
                alt="spotify-logo"
                className="spotify-login-logo">
            </img>
            {token && <p>Token : {token}</p>}
            <a href={loginUrl}>
                <button className='login-button'>Spotify Login</button>
            </a>
        </div>
    )
}

export default Login;