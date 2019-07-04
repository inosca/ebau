import Controller from "@ember/controller";
import { inject as controller } from "@ember/controller";
import { reads } from "@ember/object/computed";
import { computed } from "@ember/object";

const EDITABLE_INSTANCE_STATE_NAMES = ["In Korrektur"];

export default Controller.extend({
  editController: controller("instances.edit"),

  instanceState: reads("editController.instance.lastSuccessful.value.state"),
  case: reads("editController.data.lastSuccessful.value"),

  disabled: computed("instanceState.attributes.name", function() {
    return !EDITABLE_INSTANCE_STATE_NAMES.includes(
      this.get("instanceState.attributes.name")
    );
  })
});
