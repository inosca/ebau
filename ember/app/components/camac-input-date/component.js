import Component from "@ember/component";

export default Component.extend({
  didReceiveAttrs() {
    this.set("date", new Date(this.get("model.value")));
  },

  actions: {
    change(date) {
      this.getWithDefault("attrs.on-change", () => {})(date.toISOString());
    },
  },
});
