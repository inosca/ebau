import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { query } from "ember-data-resources";

export default class SanctionsOverviewComponent extends Component {
  @service ebauModules;

  @tracked selectedControlStep = "all";

  sanctionsQuery = query(this, "sanction", () => ({
    filter: {
      instance: this.ebauModules.instanceId,
    },
    include: "assignedService,createdByService,controlledByUser",
  }));

  sanctions(wantControlled) {
    return (this.sanctionsQuery.records ?? []).filter(
      ({ controlled, controlStep }) =>
        controlled === wantControlled &&
        (this.selectedControlStep === "all" ||
          controlStep === this.selectedControlStep),
    );
  }

  get controlledSanctions() {
    return this.sanctions(true);
  }

  get sanctionsToBeControlled() {
    return this.sanctions(false);
  }

  sanctionsCount = (step) => {
    return (this.sanctionsQuery.records ?? []).filter(
      ({ controlStep }) => step === "all" || controlStep === step,
    ).length;
  };

  get controlSteps() {
    return ["all", "baufreigabe", "realisierung", "endabnahme", "variabel"];
  }
}
