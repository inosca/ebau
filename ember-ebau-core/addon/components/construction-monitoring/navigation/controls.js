import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { confirm } from "ember-uikit";

import constructionMonitoringConfig from "ember-ebau-core/config/construction-monitoring";
import completeWorkItemMutation from "ember-ebau-core/gql/mutations/complete-work-item.graphql";
import createWorkItemMutation from "ember-ebau-core/gql/mutations/create-work-item.graphql";

export default class ConstructionMonitoringNavigationControlsComponent extends Component {
  @service ebauModules;
  @service notification;
  @service router;
  @service intl;

  @service constructionMonitoring;

  @queryManager apollo;

  config = constructionMonitoringConfig;

  @dropTask
  *createConstructionStage() {
    try {
      if (this.constructionMonitoring.constructionStages.length) {
        // Create new multiple instance task work-item construction-stage
        yield this.apollo.mutate({
          mutation: createWorkItemMutation,
          variables: {
            input: {
              case: this.constructionMonitoring.constructionStages[0].case.id,
              multipleInstanceTask:
                this.config.constructionStages.constructionStageTask,
            },
          },
        });
      } else {
        // Start construction-monitoring process
        yield this.apollo.mutate({
          mutation: completeWorkItemMutation,
          variables: {
            id: this.constructionMonitoring.controls.init.id,
          },
        });

        // Refetch stages and controls to fetch newly created stage and new status of controls
        // Isn't done through apollo watchQuery to avoid inconsistent loading states
        // where the state is switched to skipped before the stages have been fetched.
        yield this.constructionMonitoring.refetchConstructionStages();
        yield this.constructionMonitoring.refetchControls();
      }

      // Transition to new construction stage step
      yield this.constructionMonitoring.redirectToLatestConstructionStageStep();
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("construction-monitoring.construction-stage.create-error"),
      );
    }
  }

  @dropTask
  *completeConstructionMonitoring() {
    try {
      const confirmText = this.intl.t(
        "construction-monitoring.controls.complete-confirm",
      );

      if (!(yield confirm(confirmText))) {
        return;
      }

      yield this.apollo.mutate({
        mutation: completeWorkItemMutation,
        variables: {
          id: this.constructionMonitoring.controls.complete.id,
        },
      });

      // Refetch updated stages due to side effect
      yield this.constructionMonitoring.refetchConstructionStages();
      yield this.constructionMonitoring.refetchControls();
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("construction-monitoring.controls.complete-error"),
      );
    }
  }

  @dropTask
  *skipConstructionMonitoring() {
    try {
      const confirmText = this.intl.t(
        "construction-monitoring.controls.skip-confirm",
      );

      if (!(yield confirm(confirmText))) {
        return;
      }

      yield this.apollo.mutate({
        mutation: completeWorkItemMutation,
        variables: {
          id: this.constructionMonitoring.controls.init.id,
          context: JSON.stringify({
            skip: true,
          }),
        },
      });

      yield this.constructionMonitoring.refetchControls();
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("construction-monitoring.controls.skip-error"),
      );
    }
  }
}
