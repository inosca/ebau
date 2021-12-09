import Controller from "@ember/controller";
import { computed, action } from "@ember/object";
import { tracked } from "@glimmer/tracking";
import { info1, info2, info3 } from "citizen-portal/instances/new/info";
import { dropTask, restartableTask } from "ember-concurrency-decorators";

const specialFormTypes = {
  "projektgenehmigungsgesuch-gemass-ss15-strag-v3": {
    Gemeindestrassen: "municipality",
    Bezirksstrassen: "district",
    Kantonsstrassen: "canton",
  },
  "plangenehmigungsgesuch-v3": {
    ASTRA: "astra",
    "BAV (Bahnanlagen)": "bavb",
    "BAV (Schffsanlagen)": "bavs",
    BAZL: "bazl",
    ESTI: "esti",
    VBS: "vbs",
    ÜBRIGE: "uebrige",
  },
};

export default class InstancesNewController extends Controller {
  infoCol1 = info1;
  infoCol2 = info2;
  infoCol3 = info3;

  queryParams = ["group"];
  @tracked group = null;

  @tracked specialFormType = "";

  @computed("model.form.name")
  get options() {
    return specialFormTypes[this.get("model.form.name")];
  }

  @restartableTask
  *groupData() {
    if (this.get("group")) {
      return yield this.store.findRecord("group", this.get("group"), {
        include: "role,locations",
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

    if (this.specialFormType) {
      const meta = this.store.createRecord("form-field", {
        instance: model,
      });
      meta.set("name", "meta");
      meta.set("value", JSON.stringify({ formType: this.specialFormType }));
      meta.save();
    }

    yield this.transitionToRoute("instances.edit", model.id);
  }

  @action
  next() {
    if (
      [
        "projektgenehmigungsgesuch-gemass-ss15-strag-v3",
        "plangenehmigungsgesuch-v3",
      ].includes(this.get("model.form.name")) &&
      !this.specialFormType
    ) {
      return this.set("specialForm", true);
    }

    this.save.perform();
  }

  @action
  prev() {
    this.set("specialForm", false);
  }
}
