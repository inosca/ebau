import Model, { attr, belongsTo } from "@ember-data/model";
import { inject as service } from "@ember/service";
import { computed, get } from "@ember/object";
import { reads } from "@ember/object/computed";
import { dropTask } from "ember-concurrency-decorators";
import { decodeId } from "ember-caluma/helpers/decode-id";
import { ObjectQueryManager } from "ember-apollo-client";

import getInstanceDocumentsQuery from "ember-caluma-portal/gql/queries/get-instance-documents";
import saveDocumentMutation from "ember-caluma-portal/gql/mutations/save-document";

export default class Instance extends Model.extend(ObjectQueryManager) {
  @service intl;
  @service calumaStore;

  @attr() meta;
  @attr("date") creationDate;
  @attr("date") modificationDate;
  @attr("string") publicStatus;
  @belongsTo("instance-state") instanceState;

  @computed("intl.locale", "publicStatus")
  get status() {
    return this.intl.t(`instances.status.${this.publicStatus}`);
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

  @dropTask
  *createDocument(form) {
    yield this.apollo.mutate({
      mutation: saveDocumentMutation,
      variables: {
        input: {
          form,
          meta: JSON.stringify({ "camac-instance-id": parseInt(this.id) })
        }
      }
    });

    yield this.getDocuments.perform();
  }

  findCalumaField(slug, form = null) {
    const documents = form
      ? [this.calumaDocuments.find(doc => doc.rootForm.slug === form)]
      : this.calumaDocuments;

    return documents
      .filter(Boolean)
      .map(document => document.findField(slug))
      .find(Boolean);
  }
}
