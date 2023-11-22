import { inject as service } from "@ember/service";
import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

/**
 * Portal-specific instance model
 *
 * TODO: Consolidate with instance model in ember-ebau-core
 */
export default class Instance extends Model {
  @service intl;

  @attr() meta;
  @attr("date") creationDate;
  @attr("date") modificationDate;
  @attr("string") publicStatus;
  @attr("string") calumaForm;
  @attr("boolean") isPaper;
  @attr("boolean") isModification;
  @belongsTo("instance-state", { inverse: null, async: true }) instanceState;
  @belongsTo("public-service", { inverse: null, async: true }) activeService;
  @hasMany("applicant", { inverse: "instance", async: false })
  involvedApplicants;
  @attr("string") rejectionFeedback;

  get status() {
    return this.intl.t(`instances.status.${this.publicStatus}`);
  }

  get typeDetail() {
    if (!this.isPaper && !this.isModification) {
      return "";
    }
    const parts = [
      this.isPaper && this.intl.t("paper.type"),
      this.isModification && this.intl.t("modification.type"),
    ]
      .filter(Boolean)
      .join(", ");

    return `(${parts})`;
  }
}
