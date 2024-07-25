import { action } from "@ember/object";
import { service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import CfFieldInputActionButtonComponent from "@projectcaluma/ember-form/components/cf-field/input/action-button";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";
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
  @service ebauModules;
  @service fetch;
  @service intl;
  @service notification;

  @queryManager apollo;

  caseInfo = trackedFunction(this, async () => {
    const response = await this.apollo.query({
      query: getCaseMetaQuery,
      variables: { instanceId: this.args.context.instanceId },
    });

    const _case = response.allCases.edges[0]?.node;

    return { meta: _case?.meta ?? {}, form: _case?.document.form.slug };
  });

  get isPartial() {
    try {
      return (
        this.args.field.document.findAnswer("decision-approval-type") ===
        "decision-approval-type-partial-building-permit"
      );
    } catch (e) {
      return false;
    }
  }

  get isPreliminaryClarification() {
    if (macroCondition(getOwnConfig().application === "so")) {
      return ["voranfrage", "meldung"].includes(this.caseInfo.value?.form);
    }

    try {
      return (
        this.args.field.document.findAnswer("decision-workflow") ===
        "preliminary-clarification"
      );
    } catch (e) {
      return false;
    }
  }

  get isAppeal() {
    return this.caseInfo.value?.meta["is-appeal"] ?? false;
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
        }),
      );

      this.notification.success(
        this.intl.t("decision.send-notification-success"),
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
        (edge) => edge.node.case.meta,
      );

    const copiedInstanceId = copiedCaseMetas.find(
      (meta) => meta["is-rejected-appeal"],
    )["camac-instance-id"];

    this.ebauModules.redirectToInstance(copiedInstanceId);
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
      mainConfig.appeal.answerSlugs.willGenerateCopy.includes(
        this.args.field.document.findAnswer(
          mainConfig.decision.answerSlugs.decision,
        ),
      )
    ) {
      return await this.redirectToCopiedInstance();
    }

    return await super.onSuccess();
  }
}
