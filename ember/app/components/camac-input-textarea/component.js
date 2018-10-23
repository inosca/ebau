import Component from "@ember/component";

export default Component.extend({
  tagName: "textarea",

  classNames: ["uk-textarea"],

  attributeBindings: [
    "readonly:disabled",
    "config.maxlength:maxlength",
    "config.minlength:minlength",
    "config.cols:cols",
    "config.rows:rows"
  ],

  change(e) {
    e.preventDefault();

    this.getWithDefault("attrs.on-change", () => {})(e.target.value);
  }
});
