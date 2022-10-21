import React from "react";
import logo from '../images/logo512.png'

function NavBar() {
    return (
      <div className="navbar">
        <img src={logo} className="navlogo" alt="react-logo"></img>
        <h3 className="navbar-logotext">ReactFacts</h3>
        <h4 className="navbar-label">React Course - Project 1</h4>
      </div>
    );
}

export default NavBar;