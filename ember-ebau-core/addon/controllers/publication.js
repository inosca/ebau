import Controller from "@ember/controller";
import { assert } from "@ember/debug";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { queryManager, getObservable } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { DateTime, Interval } from "luxon";
import { trackedTask } from "reactiveweb/ember-concurrency";

import mainConfig from "ember-ebau-core/config/main";
import getPublications from "ember-ebau-core/gql/queries/get-publications.graphql";
import { getAnswer } from "ember-ebau-core/utils/get-answer";

export default class PublicationController extends Controller {
  @service notification;
  @service intl;
  @service ebauModules;
  @service router;

  @queryManager apollo;

  publications = trackedTask(this, this.fetchPublications, () => [
    this.variables,
  ]);

  get #config() {
    return mainConfig.publication[this.model.type];
  }

  get createTask() {
    assert(
      `A 'createTask' must be defined for type "${this.model.type}".`,
      this.#config.createTask,
    );
    return this.#config.createTask;
  }

  get instanceId() {
    return this.ebauModules.instanceId;
  }

  get variables() {
    const { task, dateRanges } = this.#config;
    assert(`A 'task' must be defined for type "${this.model.type}".`, task);

    return {
      instanceId: this.instanceId,
      task,
      dateQuestions: dateRanges.flat(),
    };
  }

  get filters() {
    return [
      { addressedGroups: [String(this.ebauModules.serviceId)] },
      {
        caseMetaValue: [{ key: "camac-instance-id", value: this.instanceId }],
      },
    ];
  }

  @action
  async refreshNavigation() {
    await this.refetchPublications.perform();
    this.router.refresh(
      this.ebauModules.resolveModuleRoute("publication", "index"),
    );
  }

  @dropTask
  *refetchPublications() {
    yield getObservable(this.publications.value).refetch();
  }

  @dropTask
  *fetchPublications(variables) {
    try {
      return yield this.apollo.watchQuery(
        { query: getPublications, variables },
        "allWorkItems.edges",
      );
    } catch {
      this.notification.danger(this.intl.t("publication.loadingError"));
    }
  }

  #getDateRanges(document) {
    const rawDates = this.#config.dateRanges
      .map((questions) => {
        return questions.map((slug) => getAnswer(document, slug)?.node.value);
      })
      .filter((dates) => dates.every(Boolean));

    const uniqueDates = [
      ...new Set(rawDates.map((dates) => dates.join(";"))),
    ].map((dates) => dates.split(";"));

    return uniqueDates.map((dates) => dates.map(DateTime.fromISO));
  }

  dateRanges = (document) => {
    return this.#getDateRanges(document)
      .map(([start, end]) => {
        return `${this.intl.formatDate(start, { format: "date" })} - ${this.intl.formatDate(end, { format: "date" })}`;
      })
      .join(", ");
  };

  dateStatus = (document) => {
    const ranges = this.#getDateRanges(document);

    if (!ranges) {
      return null;
    }

    const now = DateTime.now();
    const intervals = ranges.map((dates) => Interval.fromDateTimes(...dates));

    let status = null;
    if (intervals.some((i) => i.contains(now))) {
      status = "active";
    } else if (intervals.some((i) => i.isAfter(now))) {
      status = "future";
    } else if (intervals.some((i) => i.isBefore(now))) {
      status = "past";
    }

    return status ? this.intl.t(`publication.${status}`) : null;
  };
}
