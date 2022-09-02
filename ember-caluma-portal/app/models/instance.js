import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { lastValue, dropTask } from "ember-concurrency";
import getFormTitle from "ember-ebau-core/utils/form-title";

import config from "caluma-portal/config/environment";
import getEbauNumberQuery from "caluma-portal/gql/queries/get-ebau-number.graphql";
import getFormQuery from "caluma-portal/gql/queries/get-form.graphql";
import getSpecialFormNameAnswersQuery from "caluma-portal/gql/queries/get-special-form-name-answers.graphql";

/**
 * Portal-specific instance model
 *
 * TODO: Consolidate with instance model in ember-ebau-core
 */
export default class Instance extends Model {
  @service intl;
  @queryManager apollo;

  @attr() meta;
  @attr("date") creationDate;
  @attr("date") modificationDate;
  @attr("string") publicStatus;
  @attr("string") calumaForm;
  @attr("boolean") isPaper;
  @attr("boolean") isModification;
  @belongsTo("instance-state") instanceState;
  @belongsTo("public-service") activeService;
  @hasMany("applicant", { inverse: "instance" }) involvedApplicants;
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

  @lastValue("getMainForm") mainForm;
  @dropTask
  *getMainForm() {
    return yield this.apollo.query(
      {
        query: getFormQuery,
        variables: { form: this.calumaForm },
      },
      "allForms.edges.firstObject.node"
    );
  }

  @lastValue("fetchEbauNumber") ebauNumber = null;
  @dropTask
  *fetchEbauNumber() {
    return yield this.apollo.query(
      {
        query: getEbauNumberQuery,
        variables: { instanceId: parseInt(this.id) },
      },
      "allCases.edges.firstObject.node.meta.ebau-number"
    ) || null;
  }

  @lastValue("getSpecialFormName") specialFormName;
  @dropTask
  *getSpecialFormName() {
    const caseNode = yield this.apollo.query(
      {
        query: getSpecialFormNameAnswersQuery,
        variables: { instanceId: parseInt(this.id) },
      },
      "allCases.edges.firstObject.node"
    );
    return getFormTitle(caseNode.document, config.APPLICATION.answerSlugs);
  }
}
