import Controller from "@ember/controller";
import { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { assert } from "@ember/debug";
import { reads } from "@ember/object/computed";
import { computed } from "@ember/object";
import { task } from "ember-concurrency";
import QueryParams from "ember-parachute";
import { ObjectQueryManager } from "ember-apollo-client";
import { decodeId } from "ember-caluma/helpers/decode-id";

import getDocumentQuery from "ember-caluma-portal/gql/queries/get-document";
import saveDocumentMutation from "ember-caluma-portal/gql/mutations/save-document";

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

  setup() {
    this.documentTask.perform();
  },

  reset() {
    this.documentTask.cancelAll({ resetState: true });

    this.resetQueryParams();
  },

  embedded: computed(() => window !== window.top),

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

  disabled: computed(
    "document.form.slug",
    "instance.meta.editable-forms",
    function() {
      const form = this.get("document.form.slug");
      const editable = this.getWithDefault("instance.meta.editable-forms", []);

      return !editable.includes(form);
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
