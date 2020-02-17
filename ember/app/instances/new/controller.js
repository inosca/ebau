import Controller from "@ember/controller";
import { info1, info2, info3 } from "citizen-portal/instances/new/info";
import { task } from "ember-concurrency-decorators";

export default Controller.extend({
  infoCol1: info1,
  infoCol2: info2,
  infoCol3: info3,

  queryParams: ["group"],
  group: null,

  groupData: task(function*() {
    if (this.get("group")) {
      return yield this.store.findRecord("group", this.get("group"), {
        include: "role,locations"
      });
    }
  }).restartable(),

  @task({ restartable: true })
  *forms() {
    return yield this.store.query("form", { group: this.get("group") });
  }

  @task({ drop: true })
  *save() {
    yield this.model.save();

    const group = this.get("groupData.lastSuccessful.value");

    if (group && group.get("role.permission") === "municipality") {
      model.set("location", group.hasMany("locations").value().firstObject);
      model.set("group", group);
    }
    yield this.transitionToRoute("instances.edit", this.model.id);
  }
}
