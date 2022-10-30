import React from "react";

function Meme() {
  return (
    <div className="meme">
      <form>
        <div className="meme-top">
          <input className="meme-textbox" type="text" placeholder="Top Text" />
          <input
            className="meme-textbox"
            type="text"
            placeholder="Bottom Text"
          />
        </div>
        <button className="meme-button">Get a new meme image 🖼</button>
      </form>
    </div>
  );
}

export default Meme;
