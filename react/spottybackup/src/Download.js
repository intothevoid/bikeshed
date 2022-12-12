import React from "react";
import slogo from "./images/spotify.jpg";

import SpotifyWebApi from "spotify-web-api-js";
import JSZip from "jszip";
import { saveAs } from "file-saver";

/*
This code is creating a new instance of the Spotify Web Api library It then sets 
the access token to be used in all future calls It then gets users playlists and 
downloads them as JSON files
*/
function Download(props) {
  const logoutClicked = () => {
    window.location.href = "";
    props.updateToken(null);
  };

  const submitClicked = () => {
    // Create a new instance of the lib
    const spotifyApi = new SpotifyWebApi();

    // Get the spotify access token response from Spotify.js
    spotifyApi.setAccessToken(props.token);

    // get users playlists
    downloadPlaylistsTracks(spotifyApi);
  };

  return (
    <div className="login">
      <img src={slogo} alt="spotify-logo" className="spotify-login-logo"></img>

      <div className="control-panel">
        <input
          type="button"
          className="login-button"
          onClick={submitClicked}
          value="Download Playlists"
        />
        <input
          type="button"
          className="login-button"
          onClick={logoutClicked}
          value="Logout"
        />
      </div>
    </div>
  );
}

export default Download;

/*
This code is getting all the playlists from a user and then for each playlist it 
gets the tracks in that playlist It creates a new instance of JS Zip which is used 
to create zip files It then creates an array of promises for getting the tracks 
in each playlist For each promise it adds the name of the playlist as well as its 
data to the zip file After all promises are resolved they are all added to one big 
zip file called playlists
*/
async function downloadPlaylistsTracks(spotifyApi) {
  // get users playlists
  const playlists = await spotifyApi.getUserPlaylists();

  // Create a new instance of the JSZip library
  const zip = new JSZip();

  // Create an array of promises for getting the tracks in each playlist
  const trackPromises = playlists.items.map(async (playlist) => {
    // Get tracks in the playlist
    const tracks = await spotifyApi.getPlaylistTracks(playlist.id);

    // Add the playlist data to the zip file with the name of the playlist as the file name
    zip.file(`${playlist.name}.json`, JSON.stringify(tracks));
  });

  // Wait for all promises to be resolved
  await Promise.all(trackPromises);

  // Generate the zip file and save it
  zip.generateAsync({ type: "blob" }).then((file) => {
    saveAs(file, "playlists.zip");
  });
}
