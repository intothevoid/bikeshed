import React from "react";
import slogo from "./images/spotify.jpg"

import SpotifyWebApi from 'spotify-web-api-js';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';

function Download(props) {

    const logoutClicked = () => {
        window.location.href = "";
        props.updateToken(null);
    }

    const submitClicked = () => {
        // Create a new instance of the lib
        const spotifyApi = new SpotifyWebApi();

        // Get the spotify access token response from Spotify.js
        spotifyApi.setAccessToken(props.token);

        // get users playlists
        downloadPlaylists(spotifyApi);
    };

    return (
        <div className="login">
            <img
                src={slogo}
                alt="spotify-logo"
                className="spotify-login-logo">
            </img>

            <div className="control-panel">
                <input type="button" className="login-button" onClick={submitClicked} value="Download Playlists" />
                <input type="button" className="login-button" onClick={logoutClicked} value="Logout" />
            </div>
        </div>
    );
}

export default Download;

function downloadPlaylists(spotifyApi) {
    // get users playlists
    spotifyApi.getUserPlaylists()
        .then((playlists) => {
            // Convert the playlists object into an array using Object.values()
            const playlistArray = Object.values(playlists.items);

            // Create a new instance of the JSZip library
            const zip = new JSZip();

            // Loop through the list of playlists
            playlistArray.forEach((playlist) => {
                // Add the playlist data to the zip file with the name of the playlist as the file name
                zip.file(`${playlist.name}.json`, JSON.stringify(playlist));
            });

            // Generate the zip file and save it
            zip.generateAsync({ type: 'blob' })
                .then((file) => {
                    saveAs(file, 'playlists.zip');
                });
        }, function (err) {
            console.error(err);
        });
}
