const prom = new Promise((resolve, reject) => {
  reject();
});

prom.then(() => console.log("Success")).catch(() => console.log("Bombed out!"));

fs.promises
  .readFile("./testfile.txt", { encoding: "utf-8" })
  .then((data) => console.log(data))
  .catch((err) => console.log("An error occurred: " + err));
