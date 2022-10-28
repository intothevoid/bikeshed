import grid from '../images/photo-grid.png';
import './Hero.css';

function Hero() {
  return (
    <section className='hero'>
      <img className="hero-photo-grid" src={grid} alt='grid'></img>
      <h1 className="hero-header">Online Experiences</h1>
      <p className='hero-text'>Join unique interactive activities led by 
      one-of-a-kind hosts—all without leaving 
      home.</p>
    </section>
  );
}

export default Hero;
