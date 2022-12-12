import "./App.css";
import Login from "./Login";
import Download from "./Download";
import { useState } from "react";

/*
This code is setting the state of token to null This means that if there is no token 
then we will render a Login component If there is a token then we will render a 
Download component The reason for this is because when you log in with your Google 
account it gives you an access token which can be used to download files from google 
drive
*/
function App() {
  const [token, setToken] = useState(null);

  // This function will be called by the child component when the authorisation is complete
  const handleAuthorisationComplete = (newToken) => {
    setToken(newToken);
    console.log("Authorisation complete: " + token);
  };

  return (
    <div className="App">
      {!token && (
        <Login onAuthorisationComplete={handleAuthorisationComplete} />
      )}
      {token && (
        <Download token={token} updateToken={handleAuthorisationComplete} />
      )}
    </div>
  );
}

export default App;
