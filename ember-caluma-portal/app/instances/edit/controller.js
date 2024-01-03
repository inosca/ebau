import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { query, findRecord } from "ember-data-resources";
import mainConfig from "ember-ebau-core/config/main";
import apolloQuery from "ember-ebau-core/resources/apollo";

import config from "caluma-portal/config/environment";
import additionalDemandsCountQuery from "caluma-portal/gql/queries/get-additional-demands-count.graphql";

export default class InstancesEditController extends Controller {
  @service store;

  @queryManager apollo;

  additionalDemandsCount = apolloQuery(
    this,
    () => ({
      query: additionalDemandsCountQuery,
      fetchPolicy: "network-only",
      variables: { instanceId: this.model },
    }),
    null,
    (data) => {
      return { any: data.any.totalCount, ready: data.ready.totalCount };
    },
  );

  #instance = findRecord(this, "instance", () => [
    this.model,
    {
      include: [
        "instance_state",
        "active_service",
        "involved_applicants",
        "involved_applicants.invitee",
        "involved_applicants.user",
      ].join(","),
    },
  ]);

  #cases = useCalumaQuery(this, allCases, () => ({
    filter: [
      {
        metaValue: [{ key: "camac-instance-id", value: this.model }],
      },
    ],
  }));

  #feedbackAttachments =
    mainConfig.documentBackend === "camac"
      ? query(this, "attachment", () => ({
          instance: this.model,
          attachment_sections:
            config.APPLICATION.documents.feedbackSections.join(","),
          include: "attachment_sections",
        }))
      : query(this, "document", () => ({
          filter: {
            category: config.APPLICATION.documents.feedbackSections.join(","),
            metainfo: JSON.stringify([
              { key: "camac-instance-id", value: String(this.model) },
            ]),
          },
          include: "files,marks",
          sort: "title",
        }));

  #decisionAttachments =
    mainConfig.documentBackend === "camac"
      ? query(this, "attachment", () => ({
          instance: this.model,
          context: JSON.stringify({
            key: "isDecision",
            value: true,
          }),
          include: "attachment_sections",
        }))
      : query(this, "document", () => ({
          filter: {
            marks: mainConfig.alexandria?.marks.decision,
            metainfo: JSON.stringify([
              { key: "camac-instance-id", value: String(this.model) },
            ]),
          },
          sort: "title",
          include: "files,marks",
        }));

  #objectionAttachments = query(this, "document", () => ({
    filter: {
      marks: mainConfig.alexandria?.marks.objection,
      metainfo: JSON.stringify([
        { key: "camac-instance-id", value: String(this.model) },
      ]),
    },
    sort: "title",
    include: "files,marks",
  }));

  get hasFeedbackSection() {
    return Boolean(config.APPLICATION.documents.feedbackSections);
  }

  get case() {
    return this.#cases.value?.[0];
  }

  get instance() {
    return this.#instance.record;
  }

  get feedback() {
    if (!this.hasFeedbackSection) {
      return [];
    }

    return this.#feedbackAttachments.records;
  }

  get decision() {
    return this.#decisionAttachments.records;
  }

  get objection() {
    if (!mainConfig.alexandria?.marks.objection) {
      return [];
    }

    return this.#objectionAttachments.records;
  }

  get isLoading() {
    return (
      this.#instance.isLoading ||
      this.#cases.isLoading ||
      (this.hasFeedbackSection && this.#feedbackAttachments.isLoading) ||
      this.#decisionAttachments.isLoading
    );
  }

  reload() {
    if (this.#instance.hasRan) {
      this.#instance.retry();
    }
  }
}
