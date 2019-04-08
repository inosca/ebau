import Controller from "@ember/controller";
import { task } from "ember-concurrency";
import { info1, info2 } from "ember-caluma-portal/instances/new/info";

export default Controller.extend({
  infoCol1: info1,
  infoCol2: info2,

  selectedForm: null,

  save: task(function*() {
    const form = this.get("selectedForm");

    // TODO
  }).drop()
});
