import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { confirm } from "ember-uikit";

import cancelCaseMutation from "ember-ebau-core/gql/mutations/cancel-case.graphql";

export default class ConstructionMonitoringConstructionStageIndexController extends Controller {
  @service ebauModules;
  @service notification;
  @service router;
  @service intl;

  @service constructionMonitoring;

  @queryManager apollo;

  @dropTask
  *cancelConstructionStage() {
    try {
      const confirmText = this.intl.t(
        "construction-monitoring.construction-stage.cancel-confirm",
      );

      if (!(yield confirm(confirmText))) {
        return;
      }

      yield this.apollo.mutate({
        mutation: cancelCaseMutation,
        variables: {
          input: {
            id: this.constructionStage.childCase.id,
          },
        },
      });

      // Refetch stages to update steps
      yield this.constructionMonitoring.refetchConstructionStages();
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("construction-monitoring.construction-stage.cancel-error"),
      );
    }
  }

  get constructionStage() {
    return this.constructionMonitoring.findConstructionStage(
      this.model.constructionStageId,
    );
  }

  get infoText() {
    const key = `construction-monitoring.construction-stage.${this.constructionStage?.childCase.status.toLowerCase()}-${
      this.ebauModules.serviceId ? "service" : "applicant"
    }-info`;
    if (this.intl.exists(key)) {
      return this.intl.t(key, {
        constructionStageName: this.constructionStage.displayName,
        htmlSafe: true,
      });
    }

    return "";
  }

  get status() {
    return this.constructionMonitoring.constructionStageStatus(
      this.constructionStage,
    );
  }
}
