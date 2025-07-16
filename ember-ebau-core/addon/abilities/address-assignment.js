import { Ability } from "ember-can";

export default class AddressAssignmentAbility extends Ability {
  async canComplete() {
    if (!this.model.isReady) {
      return false;
    }

    return this.model.isAddressedToCurrentService;
  }
}
