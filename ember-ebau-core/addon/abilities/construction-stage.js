import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class ConstructionStageAbility extends Ability {
  @service ebauModules;
  @service constructionMonitoring;

  get canCreate() {
    // Check if at least one construction stage work-item (multiple-instance) is ready
    const constructionStages = this.constructionMonitoring.constructionStages;
    return (
      !this.ebauModules.isReadOnlyRole &&
      constructionStages.some((stage) => stage.status === "READY") &&
      constructionStages.every((stage) =>
        stage.addressedGroups
          .map((id) => parseInt(id))
          .includes(parseInt(this.ebauModules.serviceId)),
      )
    );
  }

  get canCancel() {
    return (
      !this.ebauModules.isReadOnlyRole &&
      this.model?.childCase.status === "RUNNING" &&
      this.model?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.ebauModules.serviceId))
    );
  }
}
