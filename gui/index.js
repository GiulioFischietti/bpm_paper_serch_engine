import templates from "./templates/index.js";

document.addEventListener("DOMContentLoaded", () => {
  const main = document.getElementById("main");
  main.innerHTML = templates.home({ name: "Pino" });
});
