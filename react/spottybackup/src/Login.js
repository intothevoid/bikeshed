import React, { useEffect, useState } from "react";
import { getTokenFromResponse, loginUrl } from "./Spotify";
import slogo from "./images/spotify.jpg";

/*
This code is setting the state of token to null The use Effect hook will run every 
time there is a change in hash which happens when you click on the login button 
This code checks if there is a new token and sets it as the value of token It then 
calls props on Authorisation Complete new Token with new Token being set to get 
Token From Response hash access token
*/
function Login(props) {
  const [token, setToken] = useState(null);
  let hash = window.location.hash;

  useEffect(() => {
    // eslint-disable-next-line react-hooks/exhaustive-deps
    hash = window.location.hash;

    if (hash !== null) {
      const newToken = getTokenFromResponse(hash).access_token;
      setToken(newToken);
      props.onAuthorisationComplete(newToken);
      console.log("Token: " + newToken);
    }
  }, [hash, token, props]);

  return (
    <div className="login">
      <img src={slogo} alt="spotify-logo" className="spotify-login-logo"></img>
      {token && <p>Token : {token}</p>}
      <a href={loginUrl}>
        <button className="login-button">Spotify Login</button>
      </a>
    </div>
  );
}

export default Login;
