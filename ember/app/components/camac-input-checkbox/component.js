import Component from "@ember/component";

export default Component.extend({
  classNames: ["uk-form-stacked"],

  actions: {
    change(
      option,
      {
        target: { checked }
      }
    ) {
      let v = this.getWithDefault("model.value", []);

      // TODO: Reject values which are not in the given options

      this.getWithDefault("attrs.on-change", () => {})([
        ...new Set([...v, option].filter(value => value !== option || checked))
      ]);
    }
  }
});
