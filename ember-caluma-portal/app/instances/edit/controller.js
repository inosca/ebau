import Controller from "@ember/controller";

export default Controller.extend({
  queryParams: ["section", "subSection"],
  section: null,
  subSection: null
});
