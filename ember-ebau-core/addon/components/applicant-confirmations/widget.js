import { action } from "@ember/object";
import { next } from "@ember/runloop";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { query } from "ember-data-resources";

import { STATUS_MAP } from "ember-ebau-core/components/applicant-confirmations/round";

export default class ApplicantConfirmationsWidget extends Component {
  @service fetch;
  @service intl;
  @service permissions;
  @service ebauModules;
  @service notification;

  @tracked showPrevious = false;
  @tracked selectedRound = null;

  statusColor = (status) => STATUS_MAP[status];

  rounds = query(this, "applicant-confirmation-round", () => ({
    document: this.args.field.document.uuid,
    include: "confirmations",
  }));

  get currentRound() {
    return this.rounds.records?.[0];
  }

  get previousRounds() {
    return this.rounds.records?.slice(1);
  }

  start = task({ drop: true }, async () => {
    try {
      await this.fetch.fetch(`/api/v1/applicant-confirmation-rounds`, {
        method: "POST",
        body: JSON.stringify({
          data: {
            type: "applicant-confirmation-rounds",
            relationships: {
              document: {
                data: {
                  id: this.args.field.document.uuid,
                  type: "documents",
                },
              },
            },
          },
        }),
      });

      this.notification.success(
        this.intl.t("applicant-confirmations.start-success"),
      );

      // We need to trigger the refresh in the next runloop as this task is being
      // awaited in `<DocumentValidityButton />` that will be destroyed as a
      // result of new permissions & rounds and therefore this task is canceled
      // before everything is refreshed
      next(this, "refresh", true);
    } catch {
      this.notification.danger(
        this.intl.t("applicant-confirmations.start-error"),
      );
    }
  });

  @action
  async refresh(withRounds = false) {
    if (withRounds) {
      // Refresh the list of rounds. This is only required if we start a new
      // round, all other actions will alter the cached store objects
      await this.rounds.retry();
    }

    // Refresh answer of confirmation question in order to trigger displaying of
    // the submit subform
    await this.args.field.refreshAnswer.perform();

    // Refresh permissions of the current instance in order to disable or enable
    // form editing
    await this.permissions.populateCacheFor(this.ebauModules.instanceId);
  }
}
