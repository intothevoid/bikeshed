import React from "react";
import logo from '../images/logo512.png'

function NavBar() {
    return (
      <div className="navbar">
        <img src={logo} className="navlogo" alt="react-logo"></img>
        <h3>ReactFacts</h3>
        <h4>React Course - Project 1</h4>
      </div>
    );
}

export default NavBar;