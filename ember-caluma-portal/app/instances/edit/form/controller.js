import Controller, { inject as controller } from "@ember/controller";
import { assert } from "@ember/debug";
import { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import QueryParams from "ember-parachute";

const queryParams = new QueryParams({
  displayedForm: {
    defaultValue: "",
    refresh: true
  }
});

export default class InstancesEditFormController extends Controller.extend(
  queryParams.Mixin
) {
  @service calumaStore;

  @controller("instances.edit") editController;
  @reads("editController.model") instanceId;
  @reads("editController.instance") instance;
  @reads("editController.instanceTask") instanceTask;

  reset() {
    this.resetQueryParams();
  }

  @computed
  get embedded() {
    return window !== window.top;
  }

  @computed("model", "instance.documents.[]")
  get document() {
    return this.getWithDefault("instance.documents", []).find(
      document => document.form.slug === this.model
    );
  }

  @computed("model")
  get pdfFieldSlug() {
    switch (this.model) {
      case "sb1":
      case "sb2":
        return "formulardownload-pdf-selbstdeklaration";
      case "vorabklaerung-einfach":
        return "formulardownload-pdf-vorabklaerung";
      default:
        return "formulardownload-pdf";
    }
  }

  @computed("pdfFieldSlug", "model", "instance.documents.[]")
  get pdfField() {
    const field = this.instance.findCalumaField(this.pdfFieldSlug, this.model);

    assert(
      `Did not find field ${this.pdfFieldSlug} in form ${this.model}`,
      field
    );

    return field;
  }
}
