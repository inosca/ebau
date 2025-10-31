import setupDeprecationWorkflow from "ember-cli-deprecation-workflow";

setupDeprecationWorkflow({
  throwOnUnhandled: true,
  workflow: [
    { handler: "silence", matchId: "new-helper-names" }, // Used in ember-leaflet
    {
      handler: "silence",
      matchId: "ember-power-select.deprecate-power-select-multiple",
    }, // until ember-power-select v9
    {
      handler: "silence",
      matchId: "ember-power-select.deprecate-power-select-multiple-input",
    }, // until ember-power-select v9
    {
      handler: "silence",
      matchId: "ember-power-select.deprecate-power-select-multiple-trigger",
    }, // until ember-power-select v9
    {
      handler: "silence",
      matchId: "ember-power-select.deprecate-input-field-placeholder-argument",
    }, // until ember-power-select v9
    {
      handler: "silence",
      matchId: "ember-power-select.no-at-ember-render-modifiers",
    }, // until ember-power-select v9
  ],
});
