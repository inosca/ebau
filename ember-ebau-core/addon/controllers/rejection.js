import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { findRecord } from "ember-data-resources";
import { localCopy } from "tracked-toolbox";

import validationsQuery from "ember-ebau-core/gql/queries/rejection/validations.graphql";
import apolloQuery from "ember-ebau-core/resources/apollo";

export default class RejectionController extends Controller {
  @service intl;
  @service store;
  @service fetch;
  @service abilities;
  @service ebauModules;
  @service notification;

  @queryManager apollo;

  @localCopy("instance.record.rejectionFeedback") feedback;

  instance = findRecord(this, "instance", () => [this.ebauModules.instanceId]);

  validations = apolloQuery(
    this,
    () => ({
      query: validationsQuery,
      fetchPolicy: "network-only",
      variables: { instanceId: this.ebauModules.instanceId },
    }),
    null,
    async (data) => {
      return {
        hasActiveDistribution: data.distribution.totalCount > 0,
        hasOpenClaims: (
          data.claims.edges[0].node.workItems.edges[0]?.node.document.answers.edges[0]?.node.value.map(
            (row) => row.answers.edges[0]?.node.value,
          ) ?? []
        ).includes("nfd-tabelle-status-in-bearbeitung"),
      };
    },
  );

  reject = dropTask(async (e) => {
    e.preventDefault();

    try {
      await this.fetch.fetch(
        `/api/v1/instances/${this.ebauModules.instanceId}/rejection`,
        {
          method: "POST",
          body: JSON.stringify({
            data: {
              id: this.ebauModules.instanceId,
              type: "instance-rejections",
              attributes: {
                "rejection-feedback": this.feedback,
              },
            },
          }),
        },
      );

      await this.instance.retry();

      this.notification.success(this.intl.t("rejection.reject-success"));

      this.refresh();
    } catch (e) {
      this.notification.danger(this.intl.t("rejection.reject-error"));
    }
  });

  revert = dropTask(async () => {
    try {
      await this.fetch.fetch(
        `/api/v1/instances/${this.ebauModules.instanceId}/rejection`,
        { method: "POST" },
      );

      await this.instance.retry();

      this.notification.success(this.intl.t("rejection.revert-success"));

      this.refresh();
    } catch (e) {
      this.notification.danger(this.intl.t("rejection.revert-error"));
    }
  });

  refresh() {
    if (this.ebauModules.applicationName === "camac-ng") {
      location.reload();
    }
  }
}
