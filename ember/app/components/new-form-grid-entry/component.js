import Component from "@ember/component";

export default Component.extend({
  tagName: "div",

  classNames: ["uk-width-1-1"],

  actions: {
    setForm(form) {
      this.onSetForm(form);
    }
  }
});
