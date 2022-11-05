import React from "react";
import memesData from "../memesData";

function Meme() {
  const [memeUrl, setMemeUrl] = React.useState("");

  function getRandomMemeUrl() {
    const randomIndex = Math.floor(Math.random() * memesData.data.memes.length);
    console.log("index" + randomIndex);
    setMemeUrl(memesData.data.memes.at(randomIndex).url);
  }

  return (
    <div className="meme">
      <div>
        <div className="meme-top">
          <input className="meme-textbox" type="text" placeholder="Top Text" />
          <input
            className="meme-textbox"
            type="text"
            placeholder="Bottom Text"
          />
        </div>
        <button className="meme-button" onClick={getRandomMemeUrl}>
          Get a new meme image 🖼
        </button>
      </div>
      <img id="meme" src={memeUrl} className="meme-img" alt="Loading meme..." />
    </div>
  );
}

export default Meme;
