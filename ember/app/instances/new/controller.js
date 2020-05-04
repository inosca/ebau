import Controller from "@ember/controller";
import { tracked } from "@glimmer/tracking";
import { info1, info2, info3 } from "citizen-portal/instances/new/info";
import { dropTask, restartableTask } from "ember-concurrency-decorators";

const specialFormTypes = {
  "projektgenehmigungsgesuch-gemass-ss15-strag": {
    Gemeindestrassen: "municipality",
    Kantonsstrassen: "canton"
  },
  plangenehmigungsgesuch: {
    ASTRA: "astra",
    ESTI: "esti",
    BAV: "bav",
    VBS: "vbs"
  }
};

export default class InstancesNewController extends Controller {
  infoCol1 = info1;
  infoCol2 = info2;
  infoCol3 = info3;

  queryParams = ["group"];
  @tracked group = null;


  specialFormType = "";

  options = computed("model.form.name", function() {
    return specialFormTypes[this.get("model.form.name")];
  });

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
    let model = this.model;

    const group = this.get("groupData.lastSuccessful.value");

    if (group && group.get("role.permission") === "municipality") {
      model.set("location", group.hasMany("locations").value().firstObject);
      model.set("group", group);
    }

    yield model.save();

    if (this.specialFormType) {
      let meta = this.store.createRecord("form-field", {
        instance: model
      });
      meta.set("name", "meta");
      meta.set("value", JSON.stringify({ formType: this.specialFormType }));
      meta.save();
    }

    yield this.transitionToRoute("instances.edit", model.id);
  }

  actions = {
    next() {
      if (
        [
          "projektgenehmigungsgesuch-gemass-ss15-strag",
          "plangenehmigungsgesuch"
        ].includes(this.get("model.form.name")) &&
        !this.specialFormType
      ) {
        return this.set("specialForm", true);
      }

      this.save.perform();
    },

    prev() {
      this.set("specialForm", false);
    }
  }
});
