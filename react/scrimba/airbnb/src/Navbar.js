import logo from './airbnb-logo.png';
import './Navbar.css';

function Navbar() {
  return (
    <div className='navbar'>
      <img className="navbar-logo" src={logo} alt='logo'></img>
      <h3>airbnb</h3>
    </div>
  );
}

export default Navbar;
