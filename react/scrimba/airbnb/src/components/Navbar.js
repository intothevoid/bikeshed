import logo from '../images/airbnb-logo.png';
import './Navbar.css';

function Navbar() {
  return (
    <nav className='navbar'>
      <img className="navbar-logo" src={logo} alt='logo'></img>
    </nav>
  );
}

export default Navbar;
