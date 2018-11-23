import Controller from "@ember/controller";
import { task } from "ember-concurrency";
import { info1, info2, info3 } from "citizen-portal/instances/new/info";

export default Controller.extend({
  infoCol1: info1,
  infoCol2: info2,
  infoCol3: info3,

  forms: task(function*() {
    return yield this.store.query("form", {});
  }).restartable(),

  save: task(function*() {
    let model = this.model;

    yield model.save();

    yield this.transitionToRoute("instances.edit", model.id);
  }).drop()
});
