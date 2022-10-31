import React from "react";
import memesData from "../memesData";

function updateMemeImage() {
  const url = getRandomMemeUrl();
  const memeImage = document.getElementById("meme");
  memeImage.src = url;
}

function getRandomMemeUrl() {
  const randomIndex = Math.floor(Math.random() * memesData.data.memes.length);
  console.log("index" + randomIndex);
  return memesData.data.memes.at(randomIndex).url;
}

function Meme() {
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
        <button className="meme-button" onClick={updateMemeImage}>
          Get a new meme image 🖼
        </button>
      </div>
      <img
        id="meme"
        src={getRandomMemeUrl()}
        className="meme-img"
        alt="Loading meme..."
      />
    </div>
  );
}

export default Meme;
