import fetch from "node-fetch";

async function getPokemonDetails(id) {
  try {
    const POKEURL = `https://pokeapi.co/api/v2/pokemon/${id}`;
    const resp = await fetch(POKEURL);
    const respJson = await resp.json();
    console.log(respJson);
  } catch (err) {
    console.error("There was an error fetching Pokemon info: " + err);
  }
}

getPokemonDetails("dittoo");
