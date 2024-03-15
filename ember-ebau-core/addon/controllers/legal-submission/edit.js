import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";
import workItemQuery from "ember-ebau-core/gql/queries/legal-submission/work-item.graphql";

export default class LegalSubmissionEditController extends Controller {
  @service notification;
  @service ebauModules;
  @service intl;

  @queryManager apollo;

  workItem = trackedFunction(this, async () => {
    try {
      const response = await this.apollo.query({
        query: workItemQuery,
        variables: {
          task: mainConfig.legalSubmission.task,
          instanceId: this.ebauModules.instanceId,
        },
      });

      return response.allWorkItems.edges[0].node;
    } catch (error) {
      this.notification.danger(this.intl.t("legal-submission.loading-error"));
    }
  });
}
