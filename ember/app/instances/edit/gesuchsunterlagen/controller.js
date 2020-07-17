import Controller from "@ember/controller";

export default Controller.extend({
  actions: {
    hideModal() {
      localStorage.setItem("hideDocumentInfo", this.hideDocumentInfo);
    },
  },
});
