import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { DateTime, Interval } from "luxon";
import { trackedTask } from "reactiveweb/ember-concurrency";

import mainConfig from "ember-ebau-core/config/main";
import getPublications from "ember-ebau-core/gql/queries/get-publications.graphql";

export default class PublicationController extends Controller {
  @service notification;
  @service intl;
  @service ebauModules;

  @queryManager apollo;

  publications = trackedTask(this, this.fetchPublications, () => [
    this.variables,
  ]);

  get variables() {
    const { task, startQuestion, endQuestion } =
      mainConfig.publication[this.model.type];

    return {
      instanceId: this.ebauModules.instanceId,
      task,
      startQuestion,
      endQuestion,
      fetchDates: Boolean(startQuestion && endQuestion),
    };
  }

  @dropTask
  *fetchPublications(variables) {
    try {
      return yield this.apollo.watchQuery(
        { query: getPublications, variables },
        "allWorkItems.edges",
      );
    } catch (error) {
      this.notification.danger(this.intl.t("publication.loadingError"));
    }
  }

  dateStatus = (startDate, endDate) => {
    if (!startDate || !endDate) {
      return null;
    }

    const interval = Interval.fromDateTimes(
      DateTime.fromISO(startDate),
      DateTime.fromISO(endDate),
    );
    const now = DateTime.now();

    const status = interval.contains(now)
      ? "active"
      : interval.isAfter(now)
        ? "future"
        : interval.isBefore(now)
          ? "past"
          : null;

    return status ? this.intl.t(`publication.${status}`) : null;
  };
}
