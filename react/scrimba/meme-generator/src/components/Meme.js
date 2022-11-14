import React from "react";
import memesData from "../memesData";

function Meme() {
  let memeInit = {
    topText: "Top Text",
    bottomText: "Bottom Text",
    randomImage: "http://i.imgflip.com/1bij.jpg",
  };

  const [allMemeImages, setAllMemeImages] = React.useState(memesData);
  const [meme, setMeme] = React.useState(memeInit);

  function getRandomMemeUrl() {
    const randomIndex = Math.floor(Math.random() * memesData.data.memes.length);
    const url = allMemeImages.data.memes.at(randomIndex).url;
    // console.log("index" + randomIndex);
    // console.log(url);

    setMeme((prevMeme) => {
      return {
        ...prevMeme,
        topText: prevMeme.topText,
        bottomText: prevMeme.bottomText,
        randomImage: url,
      };
    });
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
      <img
        id="meme"
        src={meme.randomImage}
        className="meme-img"
        alt="Loading meme..."
      />
    </div>
  );
}

export default Meme;
