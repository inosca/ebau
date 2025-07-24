import { Ability } from "ember-can";

import workItemListConfig from "ember-ebau-core/config/work-item-list";

/**
 * This is almost an exact copy of
 * `ember-ebau-core/addon/abilities/work-item.js` with minor changes to account
 * for different attributes of the dedicated work item list row model.
 */
export default class WorkItemAbility extends Ability {
  get canEdit() {
    return (
      (this.model.isReady && this.model.isAddressedToCurrentService) ||
      this.canEditAsCreatorOrController
    );
  }

  get canRead() {
    return (
      this.model.isAddressedToCurrentService ||
      this.model.isCreatedByCurrentService ||
      this.model.isControlledByCurrentService
    );
  }

  get canEditAsCreatorOrController() {
    return (
      this.model.isReady &&
      (this.model.isCreatedByCurrentService ||
        this.model.isControlledByCurrentService)
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
      workItemListConfig.completeAction &&
      this.model.isReady &&
      this.model.isAddressedToCurrentService &&
      this.model.isManuallyCompletable
    );
  }

  get canCancel() {
    return (
      this.model.isReady &&
      this.model.isCreatedByCurrentService &&
      this.model.isManuallyCompletable
    );
  }
}
