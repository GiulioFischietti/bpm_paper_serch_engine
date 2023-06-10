import rules from "./homepage.module.css" assert { type: "css" };
import utilities from "../../utils/index.js";

const styles = utilities.functions.transformCss(rules.cssRules);

const render = (/**@type {{name: string}} */ props) /**@type {string} */ => {
  return /*html*/ `<div style="${styles.myclass}">Hello ${props.name}</div>`;
};

export { render };
