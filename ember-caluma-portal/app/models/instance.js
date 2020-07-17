import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { lastValue, dropTask } from "ember-concurrency-decorators";
import gql from "graphql-tag";

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
        query: gql`
          query($form: String!) {
            allForms(slug: $form) {
              edges {
                node {
                  slug
                  name
                }
              }
            }
          }
        `,
        variables: { form: this.calumaForm },
      },
      "allForms.edges.firstObject.node"
    );
  }
}
