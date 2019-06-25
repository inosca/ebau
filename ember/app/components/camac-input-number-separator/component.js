import Component from "@ember/component";

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
    if (value === "") {
      this.set("title", "");
      return true;
    } else if (!value.match(/^-?[\d’]+[.,]?\d*$/)) {
      this.set("title", "Eingabe ist keine Zahl");
      return false;
    } else if (Number(value) > this.get("config.max")) {
      this.set("title", "Eingabe ist zu gross");
      return false;
    } else if (Number(value) < this.get("config.min")) {
      this.set("title", "Eingabe ist zu klein");
      return false;
    }
    this.set("title", "");
    return true;
  }
});
