import { service } from "@ember/service";
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
  @attr("string") name;
  @attr additionalDemandChanges;
  @belongsTo("instance-state", { inverse: null, async: true }) instanceState;
  @belongsTo("public-service", { inverse: null, async: true }) activeService;
  @hasMany("service", { inverse: null, async: true }) services;
  @hasMany("applicant", { inverse: "instance", async: false })
  involvedApplicants;
  @attr("string") rejectionFeedback;

  get status() {
    return this.intl.t(`instances.status.${this.publicStatus}`);
  }
}
