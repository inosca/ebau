import Controller from "@ember/controller";
import { computed, defineProperty } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { getOwner } from "@ember/application";
import { task } from "ember-concurrency";

import Attachment from "ember-caluma-portal/lib/attachment";
import getCaseQuery from "ember-caluma-portal/gql/queries/get-case";

const SECTION = 3;

const FeedbackAttachment = Attachment.extend({
  documentStore: service(),

  init() {
    this._super(...arguments);

    defineProperty(
      this,
      "document",
      reads(`documentStore.documents.${this.documentUuid}`)
    );
  }
});

export default Controller.extend({
  apollo: service(),
  notification: service(),
  intl: service(),
  fetch: service(),

  queryParams: ["section", "subSection", "group", "role"],
  section: null,
  subSection: null,
  group: null,
  role: null,

  isEmbedded: window !== window.top,

  headers: computed("group", "role", function() {
    return {
      ...(this.group ? { "X-CAMAC-GROUP": this.group } : {}),
      ...(this.role ? { "X-CAMAC-ROLE": this.role } : {})
    };
  }),

  data: task(function*(caseId) {
    try {
      return yield this.get("apollo").watchQuery(
        {
          query: getCaseQuery,
          fetchPolicy: "cache-and-network",
          variables: { caseId: parseInt(caseId) },
          context: { headers: this.headers }
        },
        "allCases.edges"
      );
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      this.get("notification").danger(
        this.get("intl").t("global.loadingError")
      );
    }
  }).restartable(),

  feedbackData: task(function*(caseId) {
    const response = yield this.fetch.fetch(
      `/api/v1/attachments?attachment_sections=${SECTION}&instance=${caseId}`
    );

    yield this.data.last;

    const documentId = yield this.apollo.query(
      {
        query: getCaseQuery,
        fetchPolicy: "cache-only",
        variables: { caseId: parseInt(caseId) },
        context: { headers: this.headers }
      },
      "allCases.edges.firstObject.node.document.id"
    );

    const { data } = yield response.json();

    return data.map(attachment =>
      FeedbackAttachment.create(
        getOwner(this).ownerInjection(),
        Object.assign(attachment, {
          documentUuid: atob(documentId).split(":")[1]
        })
      )
    );
  }).restartable()
});
