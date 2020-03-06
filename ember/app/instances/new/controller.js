import Controller from "@ember/controller";
import { tracked } from "@glimmer/tracking";
import { info1, info2, info3 } from "citizen-portal/instances/new/info";
import { dropTask, restartableTask } from "ember-concurrency-decorators";

export default class InstancesNewController extends Controller {
  infoCol1 = info1;
  infoCol2 = info2;
  infoCol3 = info3;

  queryParams = ["group"];
  @tracked group = null;

  @restartableTask
  *groupData() {
    if (this.get("group")) {
      return yield this.store.findRecord("group", this.get("group"), {
        include: "role,locations"
      });
    }
  }

  @restartableTask
  *forms() {
    return yield this.store.query("form", { group: this.get("group") });
  }

  @dropTask
  *save() {
    const model = this.model;

    const group = this.get("groupData.lastSuccessful.value");

    if (group && group.get("role.permission") === "municipality") {
      model.set("location", group.hasMany("locations").value().firstObject);
      model.set("group", group);
    }

    yield model.save();

    yield this.transitionToRoute("instances.edit", model.id);
  }
}
