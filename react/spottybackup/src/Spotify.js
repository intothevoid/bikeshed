// https://developer.spotify.com/documentation/web-playback-sdk/reference/

export const authEndpoint =
    "https://accounts.spotify.com/authorize";

// redirect to homepage after auth
const redirectUri = "http://localhost:3000";

const clientId = '66221beba2174873bc900c4a7e545e94';

// spotify api endpoints | permissions
// https://developer.spotify.com/documentation/general/guides/scopes/
const scopes = [
    "user-read-email",
    "user-read-private",
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "user-read-recently-played",
    "user-top-read"
];

export const getTokenFromResponse = (hash) => {
    console.log("Extracting token from URL...");
    // hash aka hash tag
    // response token = #access_token
    return hash
        //chop url into substring starting with index 1 
        .substring(1)
        // remove (character) + return array
        .split("&")
        // subtract (character) in array, starting from left
        .reduce((initial, item) => {
            let parts = item.split("=");
            // initial array returned split = and decode the key 
            initial[parts[0]] = decodeURIComponent(parts[1]);
            return initial;
        }, {});
};

// http://localhost:3000/#access_token=secret_token&token_type=Bearer&expires_in=3600
export const loginUrl = `${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scopes=${scopes.join("%20")}&response_type=token&show_dialog=true`;