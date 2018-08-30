import Component from "@ember/component";

export default Component.extend({
  tagName: "input",

  classNames: ["uk-input"],

  attributeBindings: [
    "type",
    "model.value:value",
    "readonly:disabled",
    "config.step:step",
    "config.max:max",
    "config.min:min"
  ],

  type: "number",

  change(e) {
    e.preventDefault();

    this.getWithDefault("attrs.on-change", () => {})(Number(e.target.value));
  }
});
