import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

export default class DecisionSubmitPartialComponent extends Component {
  @service fetch;
  @service intl;
  @service notifications;

  @dropTask
  *sendNotifications() {
    try {
      yield this.fetch.fetch(`/api/v1/notification-templates/sendmail`, {
        method: "POST",
        headers: {
          accept: "application/vnd.api+json",
          "content-type": "application/vnd.api+json",
        },
        body: JSON.stringify({
          data: {
            type: "notification-template-sendmails",
            attributes: {
              "template-slug": "08-entscheid-gesuchsteller",
              "recipient-types": ["applicant"],
            },
            relationships: {
              instance: {
                data: { type: "instances", id: this.args.context.instanceId },
              },
            },
          },
        }),
      });

      yield this.fetch.fetch(`/api/v1/notification-templates/sendmail`, {
        method: "POST",
        headers: {
          accept: "application/vnd.api+json",
          "content-type": "application/vnd.api+json",
        },
        body: JSON.stringify({
          data: {
            type: "notification-template-sendmails",
            attributes: {
              "template-slug": "08-entscheid-behoerden",
              "recipient-types": ["leitbehoerde", "involved_in_distribution"],
            },
            relationships: {
              instance: {
                data: { type: "instances", id: this.args.context.instanceId },
              },
            },
          },
        }),
      });
    } catch (error) {
      this.notifications.error(this.intl.t("decision.sendNotificationError"));
    }
  }
}
