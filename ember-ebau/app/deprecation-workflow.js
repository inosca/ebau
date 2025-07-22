import setupDeprecationWorkflow from "ember-cli-deprecation-workflow";

setupDeprecationWorkflow({
  throwOnUnhandled: true,
  workflow: [
    { handler: "silence", matchId: "ember-data:deprecate-array-like" }, // Used in ember-composable-helpers
    { handler: "silence", matchId: "ember-data:no-a-with-array-like" }, // Used in ember-composable-helpers
    {
      handler: "silence",
      matchId: "ember-data:deprecate-promise-many-array-behaviors",
    }, // used in ember-alexandria
    { handler: "silence", matchId: "new-helper-names" }, // Deprecation in `ember-render-helpers` used in `ember-leaflet`
  ],
});
