import katie from '../images/katie-zaferes.png'
import star from '../images/star.png'
import './Card.css';

function CardItem(props) {
    return (
      <div className="card-item">
        <img className="card-item-image" src={props.imgurl} alt="katie"></img>
        <div className="card-item-rating">
          <img className="card-item-star" src={star} alt="star"></img>
          <div className="r1">{props.r1}</div>
          <div className="r2">{props.r2}</div>
        </div>
        <div className="r3">{props.r3}</div>
        <div className="r4">{props.r4}<span className='r2'>{props.r5}</span></div>
      </div>
    );
}

function Card() {
  return (
    <section className="card">
      <CardItem
        imgurl={katie}
        r1={5.0}
        r2="(6) USA"
        r3="Life lessons with Katie Zaferes"
        r4="From $136"
        r5=" / person"
      />
    </section>
  );
}

export default Card;
