// base url
let baseURL = "http://127.0.0.1/numbers"

// elements
let saEl = document.getElementById("saBtn");
let waEl = document.getElementById("waBtn");
let vicEl = document.getElementById("vicBtn");
let nswEl = document.getElementById("nswBtn");
let tasEl = document.getElementById("tasBtn");
let ntEl = document.getElementById("ntBtn");
let actEl = document.getElementById("actBtn");

// register button clicks
registerListeners()

function registerListeners() {
  saEl.addEventListener("click", loadSANumbers);
  waEl.addEventListener("click", loadWANumbers);
  vicEl.addEventListener("click", loadVICNumbers);
  nswEl.addEventListener("click", loadNSWNumbers);
  tasEl.addEventListener("click", loadTASNumbers);
  ntEl.addEventListener("click", loadNTNumbers);
  actEl.addEventListener("click", loadACTNumbers);
}

async function loadSANumbers() {
  console.log("SA was clicked!");
  retval = await loadNumbers("sa")
  console.log(retval);
}

function loadWANumbers() {
  console.log("WA was clicked!");
}

function loadVICNumbers() {
  console.log("VIC was clicked!");
}

function loadNSWNumbers() {
  console.log("NSW was clicked!");
}

function loadTASNumbers() {
  console.log("TAS was clicked!");
}

function loadNTNumbers() {
  console.log("NT was clicked!");
}

function loadACTNumbers() {
  console.log("ACT was clicked!");
}

async function loadNumbers(state) {
    try {
        const response = await fetch(`${baseURL}/${state}`);
        if(!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        return await response.json();
    }
    catch (e) {
        console.log('loadNumbers:', e);
    }
}