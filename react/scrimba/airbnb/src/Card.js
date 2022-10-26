import katie from './katie-zaferes.png'
import star from './star.png'
import './Card.css';

function CardItem() {
    return (
      <div className="card-item">
        <img className="card-item-image" src={katie} alt="katie"></img>
        <div className="card-item-rating">
          <img className="card-item-star" src={star} alt="star"></img>
          <div className="r1">5.0</div>
          <div className="r2">(6) USA</div>
        </div>
        <div className="r3">Life lessons with Katie Zaferes</div>
        <div className="r3">From $136 / person</div>
      </div>
    );
}

function Card() {
  return (
    <section className='card'>
        <CardItem />
    </section>
  );
}

export default Card;
