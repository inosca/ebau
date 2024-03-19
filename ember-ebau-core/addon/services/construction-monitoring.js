import { action } from "@ember/object";
import Service, { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager, getObservable } from "ember-apollo-client";
import { restartableTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

import constructionMonitoringConfig from "ember-ebau-core/config/construction-monitoring";
import constructionStagesQuery from "ember-ebau-core/gql/queries/construction-monitoring/construction-stages.graphql";
import controlsQuery from "ember-ebau-core/gql/queries/construction-monitoring/controls.graphql";

export default class ConstructionMonitoringService extends Service {
  @service router;
  @service ebauModules;
  @service intl;
  @queryManager apollo;

  config = constructionMonitoringConfig;

  findConstructionStage(stageId) {
    return this.constructionStages.find(
      (stage) => decodeId(stage.id) === stageId,
    );
  }

  get isLoading() {
    return (
      !this.constructionStages.length &&
      (this.constructionStagesTask.isRunning || this.controlsTask.isRunning)
    );
  }

  constructionStepStatus(constructionStep) {
    if (!constructionStep) {
      return {};
    }

    // TODO: Improve logic implementation
    // Determine construction-step status based on latest work-item & if necessary based on stage status (applicant)
    constructionStep.sort(
      (a, b) =>
        new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime(),
    );

    const latest = constructionStep[0];
    const isLast =
      latest.meta["construction-step"].index + 1 ===
      latest.meta["construction-step"].total;
    const status =
      latest.status === "COMPLETED" && isLast
        ? "completed"
        : latest.status === "CANCELED" ||
            latest.case.parentWorkItem.status === "SKIPPED"
          ? "canceled"
          : latest.status === "READY" ||
              (latest.status === "COMPLETED" && !isLast)
            ? "in-progress"
            : "unknown";

    return {
      label: this.intl.t(this.config.STATUS_LABEL_MAP[status]),
      color: this.config.STATUS_COLOR_MAP[status],
      icon: this.config.STATUS_ICON_MAP[status],
    };
  }

  constructionStageStatus(constructionStage) {
    const childCaseStatus = constructionStage?.childCase.status;
    if (!childCaseStatus) {
      return {};
    }

    const status =
      {
        RUNNING: "in-progress",
        COMPLETED: "completed",
        CANCELED: "canceled",
      }[childCaseStatus] || "unknown";

    return {
      label: this.intl.t(this.config.STATUS_LABEL_MAP[status]),
      color: this.config.STATUS_COLOR_MAP[status],
      icon: this.config.STATUS_ICON_MAP[status],
    };
  }

  async refetchConstructionStages() {
    await getObservable(this.constructionStagesTask.value)?.refetch();
  }

  async refetchControls() {
    await getObservable(this.controlsTask.value)?.refetch();
  }

  constructionStagesTask = trackedTask(
    this,
    this.fetchConstructionStages,
    () => [this.ebauModules.instanceId],
  );

  @restartableTask
  *fetchConstructionStages(instanceId) {
    return yield this.apollo.watchQuery(
      {
        query: constructionStagesQuery,
        fetchPolicy: "cache-and-network",
        variables: {
          instanceId,
          constructionStageTask:
            this.config.constructionStages.constructionStageTask,
        },
      },
      "allWorkItems.edges",
    );
  }

  // Prepare stages with display name and step work-items
  // In the future there might be a better way to define the fields, e.g. a custom model?
  get constructionStages() {
    const stages =
      this.constructionStagesTask.value?.map(({ node }, index) => {
        const constructionSteps = this.config.constructionSteps
          .map((step) => ({
            id: step,
            workItems: node.childCase.workItems.edges
              .filter(({ node }) => node.meta["construction-step-id"] === step)
              .map(({ node }) => node),
          }))
          .filter((step) => step.workItems.length);

        const displayName = `${this.intl.t(
          "construction-monitoring.construction-stage.title",
        )} ${index + 1}${node.name !== node.task.name ? `: ${node.name}` : ""}`;

        return { ...node, displayName, constructionSteps };
      }) ?? [];

    return stages;
  }

  controlsTask = trackedTask(this, this.fetchControls, () => [
    this.ebauModules.instanceId,
  ]);

  get controls() {
    const controls = this.controlsTask.value ?? {};
    return Object.fromEntries(
      Object.entries(controls).map(([control, data]) => [
        control,
        data.edges[0]?.node,
      ]),
    );
  }

  get showNavigation() {
    return !this.isSkipped && this.isAvailable;
  }

  @restartableTask
  *fetchControls(instanceId) {
    if (!this.ebauModules.serviceId) return;

    return yield this.apollo.watchQuery({
      query: controlsQuery,
      fetchPolicy: "cache-and-network",
      variables: {
        instanceId,
        initTask: this.config.controls.initTask,
        completeTask: this.config.controls.completeTask,
        currentGroup: this.ebauModules.serviceId.toString(),
      },
    });
  }

  get isSkipped() {
    return (
      this.controls?.init?.status === "COMPLETED" &&
      !this.constructionStages?.length
    );
  }

  get isAvailable() {
    // Portal users will have no control work-items
    return this.controls?.init || this.constructionStages?.length;
  }

  @action
  async redirectToLatestConstructionStageStep() {
    if (this.constructionStagesTask.value) {
      await this.refetchConstructionStages();
    } else {
      this.constructionStagesTask.value;
      await this.fetchConstructionStages.last;
    }

    const constructionStages = this.constructionStages;
    const stage = constructionStages.at(-1);
    const step = stage?.constructionSteps.at(-1);

    if (step) {
      this.router.replaceWith(
        this.ebauModules.resolveModuleRoute(
          "construction-monitoring",
          "construction-stage.construction-step",
        ),
        decodeId(stage.id),
        step.id,
      );
    }
  }
}
