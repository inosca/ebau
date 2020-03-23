import Controller, { inject as controller } from "@ember/controller";
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
  @reads("editController.embedded") embedded;
  @reads("editController.model") instanceId;
  @reads("editController.instance") instance;
  @reads("editController.instanceTask") instanceTask;

  reset() {
    this.resetQueryParams();
  }

  @computed("model", "instance.documents.[]")
  get document() {
    return this.getWithDefault("instance.documents", []).find(
      document => document.form.slug === this.model
    );
  }
}
