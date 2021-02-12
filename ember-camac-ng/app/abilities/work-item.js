import { Ability } from "ember-can";

export default class InstanceAbility extends Ability {
  get canEdit() {
    return (
      (this.model.isReady && this.model.isAddressedToCurrentService) ||
      this.canEditAsCreator
    );
  }

  get canEditAsCreator() {
    return (
      this.model.isReady &&
      this.model.isCreatedByCurrentService &&
      this.model.raw.task.slug === "create-manual-workitems"
    );
  }

  get canAssignToMe() {
    return (
      !this.model.isAssignedToCurrentUser &&
      this.model.isAddressedToCurrentService &&
      this.model.isReady
    );
  }

  get canToggleRead() {
    return this.model.isAddressedToCurrentService && this.model.isReady;
  }

  get canComplete() {
    return (
      this.model.isReady &&
      this.model.isAddressedToCurrentService &&
      this.model.raw.task.meta["is-manually-completable"]
    );
  }
}
