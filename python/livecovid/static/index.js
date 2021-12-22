// base url
let portNo = 8000;
let baseURL = `http://127.0.0.1:${portNo}/numbers`;

// elements
let saEl = document.getElementById("saBtn");
let waEl = document.getElementById("waBtn");
let vicEl = document.getElementById("vicBtn");
let nswEl = document.getElementById("nswBtn");
let tasEl = document.getElementById("tasBtn");
let ntEl = document.getElementById("ntBtn");
let actEl = document.getElementById("actBtn");

let numbersTableEl = document.getElementById("numbersTable");
let numbersTableBodyEl = document.getElementById("numbersTableBody");
let dateLabelEl = document.getElementById("dateLabel");
let numbersLabelEl = document.getElementById("numbersLabel");
let stateNameEl = document.getElementById("stateName");

// register button clicks
registerListeners();

// load SA values by default
loadSANumbers();

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
  respObject = await loadNumbers("sa");
  populateNumbersTable(respObject);
}

async function loadWANumbers() {
  console.log("WA was clicked!");
  respObject = await loadNumbers("wa");
  populateNumbersTable(respObject);
}

async function loadVICNumbers() {
  console.log("VIC was clicked!");
  respObject = await loadNumbers("vic");
  populateNumbersTable(respObject);
}

async function loadNSWNumbers() {
  console.log("NSW was clicked!");
  respObject = await loadNumbers("nsw");
  populateNumbersTable(respObject);
}

async function loadTASNumbers() {
  console.log("TAS was clicked!");
  respObject = await loadNumbers("tas");
  populateNumbersTable(respObject);
}

async function loadNTNumbers() {
  console.log("NT was clicked!");
  respObject = await loadNumbers("nt");
  populateNumbersTable(respObject);
}

async function loadACTNumbers() {
  console.log("ACT was clicked!");
  respObject = await loadNumbers("act");
  populateNumbersTable(respObject);
}

async function loadNumbers(state) {
  try {
    const response = await fetch(`${baseURL}/${state}`);
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    return await response.json();
  } catch (e) {
    console.log("loadNumbers:", e);
  }
}

function populateNumbersTable(respObject) {
  // clear table body
  numbersTableBodyEl.innerText = "";
  numbersTableBodyEl.innerHTML = "";

  // set the state name from response
  const stateName = respObject["state"];
  stateNameEl.innerText = stateName;
  dateLabelEl.innerText = "Date";
  numbersLabelEl.innerText = "Numbers";

  const payload = respObject["payload"];

  for (key in payload) {
    const val = payload[key];
    let row = document.createElement("tr");
    let dateEl = document.createElement("td");
    let numberEl = document.createElement("td");
    dateEl.innerText = key;
    numberEl.innerText = payload[key];

    row.append(dateEl);
    row.append(numberEl);
    numbersTableBodyEl.appendChild(row);
  }
}
