import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { computed, get } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import getInstanceDocumentsQuery from "ember-caluma-portal/gql/queries/get-instance-documents";
import { decodeId } from "ember-caluma/helpers/decode-id";
import { dropTask } from "ember-concurrency-decorators";

export default class Instance extends Model {
  @service intl;
  @service calumaStore;

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

  @computed("intl.locale", "publicStatus")
  get status() {
    return this.intl.t(`instances.status.${this.publicStatus}`);
  }

  @computed("isPaper", "isModification", "intl.locale")
  get typeDetail() {
    if (!this.isPaper && !this.isModification) {
      return "";
    }
    const parts = [
      this.isPaper && this.intl.t("paper.type"),
      this.isModification && this.intl.t("modification.type")
    ]
      .filter(Boolean)
      .join(", ");

    return `(${parts})`;
  }

  @computed("documents.[]")
  get mainForm() {
    const document =
      this.documents &&
      this.documents.find(doc => get(doc, "form.meta.is-main-form"));

    return document && document.form;
  }

  @computed("documents.@each.id")
  get calumaDocuments() {
    return this.getWithDefault("documents", [])
      .map(({ id }) => {
        return this.calumaStore.find(`Document:${decodeId(id)}`);
      })
      .filter(Boolean);
  }

  @reads("getDocuments.lastSuccessful.value") documents;
  @dropTask()
  *getDocuments() {
    const raw = yield this.apollo.query({
      query: getInstanceDocumentsQuery,
      fetchPolicy: "network-only",
      variables: {
        instanceId: parseInt(this.id)
      }
    });

    return raw.allDocuments.edges.map(({ node }) => node);
  }
}
