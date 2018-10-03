import Controller from "@ember/controller";
import { task } from "ember-concurrency";

export default Controller.extend({
  infoCol1: "Platzhalter Information Vorstufe",
  infoCol2: "Platzhalter Information Baubewilligung",
  infoCol3: "Platzhalter Information speziell",

  forms: task(function*() {
    return yield this.store.query("form", {});
  }).restartable(),

  save: task(function*() {
    let model = this.model;

    yield model.save();

    yield this.transitionToRoute("instances.edit", model.id);
  }).drop()
});
