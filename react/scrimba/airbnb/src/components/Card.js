import star from '../images/star.png'
import './Card.css';
import data from '../data'

function CardItem(props) {
  let badgeText
  if (props.openSpots === 0)
  {
    badgeText = "SOLD OUT";
  }
  else if (props.location === "Online") {
    badgeText = "ONLINE";
  }
    return (
      <div className="card-item">
        {badgeText && <div className='card-item-badge'>{badgeText}</div>}
        <img className="card-item-image" src={props.img} alt="thumbnail"></img>
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
  const dataElements = data.map((item, i) => {
    return (
      <CardItem
        key={i}
        id={item.id}
        img={item.coverImg}
        r1={item.stats.rating}
        r2={`(${item.stats.reviewCount}) ${item.location}`}
        r3={item.title}
        r4={`From ${item.price}`}
        r5=" / person"
        openSpots={item.openSpots}
      />
    )
  });

  return <section className='card-list'>{dataElements}</section>;
}

export default Card;
