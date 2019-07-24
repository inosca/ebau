import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { assert } from "@ember/debug";
import { computed, get } from "@ember/object";
import { reads } from "@ember/object/computed";
import { task } from "ember-concurrency";
import QueryParams from "ember-parachute";
import { ObjectQueryManager } from "ember-apollo-client";

import getDocumentQuery from "ember-caluma-portal/gql/queries/get-document";

const VISIBLE_MAP = {
  internal: {
    sb1: ["Abschluss (SB2)", "Zum Abschluss", "Abgeschlossen"],
    sb2: ["Zum Abschluss", "Abgeschlossen"]
  },
  DEFAULT: {
    sb1: [
      "Selbstdeklaration (SB1)",
      "Abschluss (SB2)",
      "Zum Abschluss",
      "Abgeschlossen"
    ],
    sb2: ["Abschluss (SB2)", "Zum Abschluss", "Abgeschlossen"]
  }
};

const FEEDBACK_ATTACHMENT_SECTION = 3;

const queryParams = new QueryParams({
  group: {
    default: null,
    refresh: true
  },
  role: {
    default: null,
    refresh: true
  }
});

export default Controller.extend(queryParams.Mixin, ObjectQueryManager, {
  fetch: service(),

  setup() {
    this.mainFormTask.perform();
    this.instanceTask.perform();
    this.feedbackTask.perform();
  },

  reset() {
    this.mainFormTask.cancelAll({ resetState: true });
    this.instanceTask.cancelAll({ resetState: true });
    this.feedbackTask.cancelAll({ resetState: true });

    this.resetQueryParams();
  },

  additionalForms: computed(
    "instance.state.attributes.name",
    "role",
    function() {
      const state = this.get("instance.state.attributes.name");
      const role = this.role || "DEFAULT";

      return Object.entries(VISIBLE_MAP[role])
        .filter(([, visibleStates]) => visibleStates.includes(state))
        .map(([form]) => form);
    }
  ),

  mainForm: reads("mainFormTask.lastSuccessful.value"),
  mainFormTask: task(function*() {
    const [document] = (yield this.apollo.query(
      {
        query: getDocumentQuery,
        fetchPolicy: "cache-first",
        variables: { instanceId: this.model }
      },
      "allDocuments.edges"
    ))
      .map(edge => edge.node)
      .filter(doc => get(doc, "form.meta.is-main-form"));

    assert("Document for main form not found", document);

    return document.form;
  }).drop(),

  instance: reads("instanceTask.lastSuccessful.value"),
  instanceTask: task(function*() {
    const groupParam = this.group ? "&group=" + this.group : "";
    const response = yield this.fetch.fetch(
      `/api/v1/instances/${this.model}?include=instance_state${groupParam}`
    );

    const { included, data: instance } = yield response.json();

    return {
      ...instance.attributes,
      id: instance.id,
      state: included.find(
        obj =>
          obj.type === "instance-states" &&
          obj.id === instance.relationships["instance-state"].data.id
      )
    };
  }).drop(),

  feedback: reads("feedbackTask.lastSuccessful.value"),
  feedbackTask: task(function*() {
    const response = yield this.fetch.fetch(
      `/api/v1/attachments?attachment_sections=${FEEDBACK_ATTACHMENT_SECTION}&instance=${this.model}`
    );

    const { data } = yield response.json();

    return data;
  }).drop()
});
