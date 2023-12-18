import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, restartableTask, timeout } from "ember-concurrency";
import { findRecord } from "ember-data-resources";
import { confirm } from "ember-uikit";
import { localCopy } from "tracked-toolbox";

import validationsQuery from "ember-ebau-core/gql/queries/rejection/validations.graphql";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
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
      variables: {
        instanceId: this.ebauModules.instanceId,
        useLegacyClaims: hasFeature("rejection.useLegacyClaims"),
      },
    }),
    null,
    async (data) => {
      return {
        hasActiveDistribution: data.distribution.totalCount > 0,
        hasOpenClaims: hasFeature("rejection.useLegacyClaims")
          ? (
              data.legacyClaims.edges[0].node.workItems.edges[0]?.node.document.answers.edges[0]?.node.value.map(
                (row) => row.answers.edges[0]?.node.value,
              ) ?? []
            ).includes("nfd-tabelle-status-in-bearbeitung")
          : data.claims.totalCount > 0,
      };
    },
  );

  @restartableTask
  *save() {
    yield timeout(500);
    yield this.fetch.fetch(
      `/api/v1/instances/${this.ebauModules.instanceId}/rejection`,
      {
        method: "PATCH",
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
  }

  reject = dropTask(async (e) => {
    e.preventDefault();

    if (
      !hasFeature("rejection.revert") &&
      !(await confirm(this.intl.t("rejection.reject-confirm")))
    ) {
      return;
    }

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
