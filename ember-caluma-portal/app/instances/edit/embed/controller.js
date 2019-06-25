import Controller from "@ember/controller";
import { inject as controller } from "@ember/controller";
import { reads } from "@ember/object/computed";
import { computed } from "@ember/object";

const EDITABLE_INSTANCE_STATE_NAMES = ["In Korrektur"];

export default Controller.extend({
  editController: controller("instances.edit"),

  instanceState: reads("editController.instanceState"),
  case: reads("editController.data.lastSuccessful.value"),

  disabled: computed("instanceState.lastSuccessful.value", function() {
    return !EDITABLE_INSTANCE_STATE_NAMES.includes(
      this.get("instanceState.lastSuccessful.value.attributes.name")
    );
  })
});
