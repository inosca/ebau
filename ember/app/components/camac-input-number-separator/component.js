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
    "title",
  ],

  type: "text",

  title: "",
  displayValue: "",

  didReceiveAttrs() {
    this.set(
      "displayValue",
      Number(
        this.get("model.value") ? this.get("model.value") : 0
      ).toLocaleString("de-CH")
    );
  },

  change(e) {
    e.preventDefault();

    this.getWithDefault("attrs.on-change", () => {})(
      Number(e.target.value.replace(/,/, "."))
    );
  },

  focusIn(e) {
    this.set("displayValue", e.target.value.replace(/’/g, ""));
  },

  focusOut(e) {
    if (!e.target.value.match(/’/)) {
      this.set(
        "displayValue",
        Number(e.target.value.replace(/,/, ".")).toLocaleString("de-CH")
      );
    }
  },
});
