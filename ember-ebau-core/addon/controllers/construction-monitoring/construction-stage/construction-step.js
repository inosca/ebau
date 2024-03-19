import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager, getObservable } from "ember-apollo-client";
import { dropTask, restartableTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

import completeWorkItemMutation from "ember-ebau-core/gql/mutations/complete-work-item.graphql";
import saveWorkItemMutation from "ember-ebau-core/gql/mutations/save-workitem.graphql";
import constructionStageNameQuery from "ember-ebau-core/gql/queries/construction-monitoring/construction-stage-name.graphql";
import constructionStepQuery from "ember-ebau-core/gql/queries/construction-monitoring/construction-step.graphql";

export default class ConstructionMonitoringConstructionStageConstructionStepController extends Controller {
  @service ebauModules;
  @service notification;
  @service router;
  @service intl;
  @service store;
  @service constructionMonitoring;

  @queryManager apollo;

  async refetchConstructionStep() {
    await getObservable(this.constructionStepTask.value)?.refetch();
  }

  constructionStepTask = trackedTask(this, this.fetchConstructionStep, () => [
    this.model.constructionStageId,
    this.model.constructionStageChildCaseId,
    this.model.constructionStepId,
  ]);

  userTask = trackedTask(this, this.fetchUsers, () => [this.userIds]);

  serviceTask = trackedTask(this, this.fetchServices, () => [this.serviceIds]);

  @restartableTask
  *fetchUsers(users) {
    yield Promise.resolve();
    if (!users.length) {
      return [];
    }

    return [
      ...(yield this.store.query("public-user", {
        username: users.join(","),
      }) ?? []),
    ];
  }

  @restartableTask
  *fetchServices(services) {
    yield Promise.resolve();
    if (!services.length) {
      return [];
    }

    return [
      ...(yield this.store.query("public-service", {
        service_id: services.join(","),
      }) ?? []),
    ];
  }

  @restartableTask
  *fetchConstructionStep(
    constructionStageId,
    constructionStageChildCaseId,
    constructionStepId,
  ) {
    return yield this.apollo.watchQuery(
      {
        query: constructionStepQuery,
        fetchPolicy: "cache-and-network",
        variables: {
          caseId: constructionStageChildCaseId,
          constructionStepId,
          questionId: `${constructionStepId}-is-approved`,
        },
      },
      "allWorkItems.edges",
    );
  }

  get constructionStepWorkItemGroups() {
    const workItems = this.constructionStep ?? [];

    // divide work-items into groups
    const groups = [];
    workItems.forEach((w) => {
      if (w.meta["construction-step"].index === 0) {
        // add next group with first work-item
        groups.push([w]);
      } else {
        // add next work-item to last added group
        groups.at(-1).push(w);
      }
    });

    // sort group work-items by construction-step-index in descending order
    groups.forEach((group) =>
      group.sort(
        (a, b) =>
          b.meta["construction-step"].index - a.meta["construction-step"].index,
      ),
    );

    // sort groups by creation date in descending order
    groups.sort(
      (a, b) =>
        new Date(b[0].createdAt).getTime() - new Date(a[0].createdAt).getTime(),
    );

    return groups;
  }

  get lastWorkItemId() {
    // TODO: Improve logic implementation
    // Retrieve latest work-item of latest group
    return this.constructionStepWorkItemGroups?.[0]?.[0]?.id;
  }

  @dropTask
  *completeConstructionStepWorkItem(workItem, validate = () => true) {
    try {
      if (typeof validate === "function" && !(yield validate())) return;

      if (workItem.task.slug === "construction-step-plan-construction-stage") {
        yield this.updateConstructionStageName.perform(workItem);
      }

      yield this.apollo.mutate({
        mutation: completeWorkItemMutation,
        variables: {
          id: decodeId(workItem.id),
        },
      });

      yield this.refetchConstructionStep();
      yield this.constructionMonitoring.refetchConstructionStages();
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t(`construction-monitoring.construction-step.complete-error`),
      );
    }
  }

  @dropTask
  *updateConstructionStageName(workItem) {
    try {
      const documents = yield this.apollo.query(
        {
          query: constructionStageNameQuery,
          variables: { id: workItem.document.id },
        },
        "allDocuments.edges",
      );

      const constructionStageName =
        documents[0]?.node.constructionStageName.edges[0]?.node.value ?? "";

      // Stage name updated in navigation because it is
      // returned in save-work-item mutation
      yield this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.model.constructionStageId,
            name: constructionStageName,
          },
        },
      });
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t(
          "construction-monitoring.construction-step.update-construction-stage-name-error",
        ),
      );
    }
  }

  get constructionStepName() {
    return this.intl.t(
      `construction-monitoring.construction-step.${this.model.constructionStepId}`,
    );
  }

  get constructionStep() {
    return this.constructionStepTask.value?.map((workItem) => workItem.node);
  }

  get userIds() {
    return [
      ...new Set(
        (this.constructionStep || [])
          .filter((workItem) => workItem.status === "COMPLETED")
          .map((workItem) => workItem.closedByUser)
          .filter(Boolean),
      ),
    ];
  }

  get serviceIds() {
    return [
      ...new Set(
        (this.constructionStep || [])
          .filter((workItem) => workItem.status === "COMPLETED")
          .map((workItem) => workItem.closedByGroup)
          .filter(Boolean),
      ),
    ];
  }

  get users() {
    return this.userTask.value ?? [];
  }

  get services() {
    return this.serviceTask.value ?? [];
  }

  get status() {
    return this.constructionMonitoring.constructionStepStatus(
      this.constructionStep,
    );
  }

  get constructionStage() {
    return this.constructionMonitoring.findConstructionStage(
      this.model.constructionStageId,
    );
  }
}
