import Controller from "@ember/controller";
import { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { assert } from "@ember/debug";
import { reads, equal } from "@ember/object/computed";
import { computed, getWithDefault } from "@ember/object";
import { task } from "ember-concurrency";
import QueryParams from "ember-parachute";
import { ObjectQueryManager } from "ember-apollo-client";
import { decodeId } from "ember-caluma/helpers/decode-id";

import getDocumentQuery from "ember-caluma-portal/gql/queries/get-document";
import saveDocumentMutation from "ember-caluma-portal/gql/mutations/save-document";

const EDITABLE_MAP = {
  internal: {
    sb1: [],
    sb2: [],

    MAIN: ["In Korrektur"]
  },
  DEFAULT: {
    sb1: ["Selbstdeklaration (SB1)"],
    sb2: ["Abschluss (SB2)"],

    MAIN: ["Neu", "Zurückgewiesen"]
  }
};

const queryParams = new QueryParams({
  displayedForm: {
    default: "",
    refresh: true
  }
});

export default Controller.extend(queryParams.Mixin, ObjectQueryManager, {
  calumaStore: service(),

  editController: controller("instances.edit"),
  instanceId: reads("editController.model"),
  instance: reads("editController.instance"),
  role: reads("editController.role"),

  setup() {
    this.documentTask.perform();
  },

  reset() {
    this.documentTask.cancelAll({ resetState: true });

    this.resetQueryParams();
  },

  document: reads("documentTask.lastSuccessful.value"),
  documentTask: task(function*() {
    return yield this.apollo.query(
      {
        query: getDocumentQuery,
        fetchPolicy: "network-only",
        variables: { form: this.model, instanceId: this.instanceId }
      },
      "allDocuments.edges.firstObject.node"
    );
  }).drop(),

  createDocument: task(function*() {
    yield this.apollo.mutate({
      mutation: saveDocumentMutation,
      variables: {
        input: {
          form: this.model,
          meta: JSON.stringify({ "camac-instance-id": this.instanceId })
        }
      }
    });

    yield this.documentTask.perform();
  }),

  internal: equal("role", "internal"),

  disabled: computed(
    "document.form.{slug,meta.is-main-form}",
    "instance.state.attributes.name",
    "role",
    function() {
      const state = this.get("instance.state.attributes.name");
      const form = this.get("document.form.meta.is-main-form")
        ? "MAIN"
        : this.get("document.form.slug");
      const role = this.role || "DEFAULT";

      return !getWithDefault(EDITABLE_MAP, `${role}.${form}`, []).includes(
        state
      );
    }
  ),

  pdfField: computed("document", function() {
    const document = this.calumaStore.find(
      `Document:${decodeId(this.document.id)}`
    );

    assert(
      `Did not find document ${decodeId(this.document.id)} in calumaStore`,
      document
    );

    const slug = ["sb1", "sb2"].includes(this.model)
      ? "formulardownload-pdf-selbstdeklaration"
      : "formulardownload-pdf";

    const field = document.findField(slug);

    assert(`Did not find field ${slug} in document ${document.uuid}`, field);

    return field;
  })
});
