import Controller, { inject as controller } from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";

import { confirmTask } from "camac-ng/decorators";
import completeWorkItem from "camac-ng/gql/mutations/complete-work-item.graphql";
import skipWorkItem from "camac-ng/gql/mutations/skip-work-item.graphql";

export default class AuditIndexController extends Controller {
  @service notifications;
  @service intl;
  @service fetch;

  @queryManager apollo;

  @controller("audit") auditController;

  @tracked showSameEbauNumber = false;

  @dropTask
  @confirmTask("audit.skipConfirm")
  *skipAudit() {
    try {
      yield this.apollo.mutate({
        mutation: skipWorkItem,
        variables: { id: this.auditController.auditWorkItem.id },
      });

      yield this.auditController.fetchAudit.perform();

      this.notifications.success(this.intl.t("audit.skipSuccess"));
    } catch (error) {
      this.notifications.error(this.intl.t("audit.skipError"));
    }
  }

  @dropTask
  @confirmTask("audit.completeConfirm")
  *completeAudit() {
    try {
      yield this.apollo.mutate({
        mutation: completeWorkItem,
        variables: { id: this.auditController.auditWorkItem.id },
      });

      yield this.auditController.fetchAudit.perform();

      this.notifications.success(this.intl.t("audit.completeSuccess"));
    } catch (error) {
      if (error.errors) {
        // validation failed
        this.notifications.error(this.intl.t("audit.completeInvalid"));
      } else {
        // generic error
        this.notifications.error(this.intl.t("audit.completeError"));
      }
    }
  }

  @action
  toggleShowSameEbauNumber() {
    this.showSameEbauNumber = !this.showSameEbauNumber;
  }
}
