import setupDeprecationWorkflow from "ember-cli-deprecation-workflow";

setupDeprecationWorkflow({
  throwOnUnhandled: true,
  workflow: [
    { handler: "silence", matchId: "new-helper-names" }, // Used in ember-leaflet
  ],
});
