import Controller from "@ember/controller";
import { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { assert } from "@ember/debug";
import { reads } from "@ember/object/computed";
import { computed } from "@ember/object";
import { queryParam } from "ember-parachute/decorators";

export default class InstancesEditFormController extends Controller {
  @queryParam({ refresh: true }) displayedForm = "";

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

  @computed("model", "instance.documents.[]")
  get pdfField() {
    const slug = ["sb1", "sb2"].includes(this.model)
      ? "formulardownload-pdf-selbstdeklaration"
      : this.model === "vorabklaerung-einfach"
      ? "formulardownload-pdf-vorabklaerung"
      : "formulardownload-pdf";

    const field = this.instance.findCalumaField(slug, this.model);

    assert(`Did not find field ${slug} in form ${this.model}`, field);

    return field;
  }
}
