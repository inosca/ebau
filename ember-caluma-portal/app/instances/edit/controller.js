import Controller from "@ember/controller";

export default Controller.extend({
  queryParams: ["section", "subSection", "group", "role"],
  section: null,
  subSection: null,
  group: null,
  role: null,

  isEmbedded: window !== window.top
});
