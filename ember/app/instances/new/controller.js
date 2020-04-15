import Controller from "@ember/controller";
import { task } from "ember-concurrency";
import { info1, info2, info3 } from "citizen-portal/instances/new/info";

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

  forms: task(function*() {
    return yield this.store.query("form", { group: this.get("group") });
  }).restartable(),

  save: task(function*() {
    let model = this.model;

    const group = this.get("groupData.lastSuccessful.value");

    if (group.get("role.permission") === "municipality") {
      model.set("location", group.hasMany("locations").value().firstObject);
      model.set("group", group);
    }

    yield model.save();

    yield this.transitionToRoute("instances.edit", model.id);
  }).drop()
});
