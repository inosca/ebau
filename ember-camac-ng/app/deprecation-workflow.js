import setupDeprecationWorkflow from "ember-cli-deprecation-workflow";

setupDeprecationWorkflow({
  throwOnUnhandled: true,
  workflow: [
    { handler: "silence", matchId: "remove-owner-inject" },
    { handler: "silence", matchId: "ember-polyfills.deprecate-assign" }, // Used in ember-data v3 and ember-simple-auth
    { handler: "silence", matchId: "ember-modifier.no-element-property" }, // Used in ember-autoresize-modifier
    { handler: "silence", matchId: "ember-modifier.use-modify" }, // Used in ember-gesture-modifiers via ember-toggle via ember-uikit
    { handler: "silence", matchId: "ember-modifier.no-args-property" }, // Used in ember-gesture-modifiers via ember-toggle via ember-uikit
    { handler: "silence", matchId: "ember-data:deprecate-early-static" }, // Used in ember-cli-mirage
    { handler: "silence", matchId: "ember-data:deprecate-promise-proxies" }, // Used in ember-power-select
  ],
});
