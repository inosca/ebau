import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { isTesting, macroCondition } from "@embroider/macros";
import CfFieldInputActionButtonComponent from "@projectcaluma/ember-form/components/cf-field/input/action-button";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import getCaseMetaQuery from "ember-ebau-core/gql/queries/get-case-meta.graphql";
import getCopiesQuery from "ember-ebau-core/gql/queries/get-copies.graphql";

const PARTIAL_NOTIFICATION_CONFIG = [
  {
    "template-slug": "08-entscheid-gesuchsteller",
    "recipient-types": ["applicant"],
  },
  {
    "template-slug": "08-entscheid-behoerden",
    "recipient-types": ["leitbehoerde", "involved_in_distribution"],
  },
];

export default class DecisionSubmitButtonComponent extends CfFieldInputActionButtonComponent {
  @service fetch;
  @service intl;
  @service notification;

  @queryManager apollo;

  caseMeta = trackedFunction(this, async () => {
    const response = await this.apollo.query({
      query: getCaseMetaQuery,
      variables: { instanceId: this.args.context.instanceId },
    });

    return response.allCases.edges[0]?.node.meta ?? {};
  });

  get isPartial() {
    return (
      this.args.field.document.findAnswer("decision-approval-type") ===
      "decision-approval-type-partial-building-permit"
    );
  }

  get isPreliminaryClarification() {
    return (
      this.args.field.document.findAnswer("decision-workflow") ===
      "preliminary-clarification"
    );
  }

  get isAppeal() {
    return this.caseMeta.value?.["is-appeal"] ?? false;
  }

  get label() {
    if (this.isAppeal) {
      return this.intl.t("decision.submit.appeal");
    } else if (this.isPreliminaryClarification) {
      return this.intl.t("decision.submit.preliminary-clarification");
    }

    return this.args.field.question.raw.label;
  }

  async sendNotifications() {
    try {
      await Promise.all(
        PARTIAL_NOTIFICATION_CONFIG.map((data) => {
          return this.fetch.fetch(`/api/v1/notification-templates/sendmail`, {
            method: "POST",
            headers: {
              accept: "application/vnd.api+json",
              "content-type": "application/vnd.api+json",
            },
            body: JSON.stringify({
              data: {
                type: "notification-template-sendmails",
                attributes: data,
                relationships: {
                  instance: {
                    data: {
                      type: "instances",
                      id: this.args.context.instanceId,
                    },
                  },
                },
              },
            }),
          });
        })
      );
    } catch (error) {
      this.notification.danger(this.intl.t("decision.send-notification-error"));
    }
  }

  async redirectToCopiedInstance() {
    const response = await this.apollo.query({
      query: getCopiesQuery,
      variables: { instanceId: this.args.context.instanceId },
    });

    const copiedCaseMetas =
      response.allCases.edges[0].node.document.copies.edges.map(
        (edge) => edge.node.case.meta
      );

    const copiedInstanceId = copiedCaseMetas.find(
      (meta) => meta["is-rejected-appeal"]
    )["camac-instance-id"];

    if (macroCondition(isTesting())) {
      this.args.redirectTo(copiedInstanceId);
    } else {
      window.location.replace(
        `/index/redirect-to-instance-resource/instance-id/${copiedInstanceId}`
      );
    }
  }

  @action
  async beforeMutate(validateFn) {
    const result = await super.beforeMutate(validateFn);

    if (this.isPartial) {
      await this.sendNotifications();

      // return to make sure the work item won't be completed
      return false;
    }

    return result;
  }

  @action
  async onSuccess() {
    if (
      this.isAppeal &&
      this.args.field.document.findAnswer("decision-decision-assessment") ===
        "decision-decision-assessment-appeal-rejected"
    ) {
      return await this.redirectToCopiedInstance();
    }

    return await super.onSuccess();
  }
}
