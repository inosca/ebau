import Component from "@ember/component";
import validations from "citizen-portal/questions/validations";

// The component to display numbers with thousands separators
export default Component.extend({
  tagName: "input",

  classNames: ["uk-input"],
  classNameBindings: ["title:uk-form-danger"],

  attributeBindings: [
    "type",
    "displayValue:value",
    "readonly:disabled",
    "title"
  ],

  type: "text",

  title: "",
  displayValue: "",

  didReceiveAttrs() {
    this._super(...arguments);
    this.set(
      "displayValue",
      Number(this.get("model.value")).toLocaleString("de-CH")
    );
  },

  change(e) {
    e.preventDefault();

    if (this.validateValue(e.target.value)) {
      this.getWithDefault("attrs.on-change", () => {})(
        Number(e.target.value.replace(/,/, "."))
      );
    }
  },

  focusIn(e) {
    this.set("displayValue", e.target.value.replace(/’/g, ""));
  },

  focusOut(e) {
    if (this.validateValue(e.target.value) && !e.target.value.match(/’/)) {
      this.set("displayValue", Number(e.target.value).toLocaleString("de-CH"));
    }
  },

  validateValue(value) {
    let result = validations.validateNumberSeparator(
      { min: this.get("config.min"), max: this.get("config.max") },
      value
    );
    this.set("title", result);
    return !result;
  }
});
