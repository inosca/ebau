import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class extends Ability {
  @service shoebox;

  get canEdit() {
    return (
      this.model.status === "READY" &&
      !this.shoebox.isReadOnlyRole &&
      this.model.addressedGroups.find(
        (groupId) =>
          parseInt(groupId) === parseInt(this.shoebox.content.serviceId)
      )
    );
  }
}
