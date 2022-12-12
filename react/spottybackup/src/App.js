import "./App.css";
import Login from "./Login";
import Download from "./Download";
import { useState } from "react";

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
