import Component from "@ember/component";

export default Component.extend({
  tagName: "input",

  classNames: ["uk-input"],

  attributeBindings: [
    "type",
    "model.value:value",
    "readonly:disabled",
    "config.max:max",
    "config.min:min"
  ],

  type: "date",

  change(e) {
    e.preventDefault();

    this.getWithDefault("attrs.on-change", () => {})(e.target.value);
  }
});
