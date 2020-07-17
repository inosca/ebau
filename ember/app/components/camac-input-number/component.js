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
    "config.min:min",
  ],

  type: "number",

  init(...args) {
    /**
     * If no step is set, decimal numbers are not allowed.
     * So if not a specific step is defined, fallback to 0.01,
     * this way decimal numbers with two numbers after the point are allowed.
     */
    if (!this.get("config.step")) {
      this.set("config.step", 0.01);
    }
    this._super(...args);
  },

  change(e) {
    e.preventDefault();

    this.getWithDefault("attrs.on-change", () => {})(Number(e.target.value));
  },
});
