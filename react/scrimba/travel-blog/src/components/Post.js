import React from 'react';

function Post(props) {
  return (
    <div className="post">
      <img className="post-img" src={props.imageUrl} alt="Japan"></img>
      <div className="info">
        <div className="pinlocurl">
          <img className="pin" src="./pin.png" alt="pin"></img>
          <div className="location">{props.location.toUpperCase()}</div>
          <a className="google-link" href={props.googleMapsUrl} target="_link">
            View on Google Maps
          </a>
        </div>
        <div className="title">{props.title}</div>
        <div className='date-range'>{props.startDate} - {props.endDate}</div>
        <div className='description'>{props.description}</div>
      </div>
    </div>
  );
}

export default Post;