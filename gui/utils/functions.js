function transformCss(/**@type {CSSRuleList} */ rules) {
  const result = {};
  for (let i = 0; i < rules.length; i++) {
    const ruleItem = rules.item(i);
    result[ruleItem.selectorText.substring(1)] = ruleItem.cssText.split(" ").slice(1).join(" ").replace(/[{}]/g, "").trim();
  }
  return result;
}

export default { transformCss };
