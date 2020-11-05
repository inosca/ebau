import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import getAudit from "camac-ng/gql/queries/get-audit";

export default class AuditController extends Controller {
  @service store;
  @service shoebox;
  @service notifications;

  @queryManager apollo;

  get disabled() {
    return (
      this.auditWorkItem?.status !== "READY" ||
      !this.auditWorkItem.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.shoebox.content.serviceId))
    );
  }

  @lastValue("fetchAudit") auditWorkItem;
  @dropTask
  *fetchAudit() {
    try {
      const response = yield this.apollo.query({
        query: getAudit,
        fetchPolicy: "network-only",
        variables: { instanceId: this.model },
      });

      const workItem = response.allCases.edges[0].node.workItems.edges[0].node;

      yield this.fetchAdditionalData.perform(workItem);

      return workItem;
    } catch (error) {
      this.notifications.error(this.intl.t("audit.loadingError"));
    }
  }

  @dropTask
  *fetchAdditionalData(workItem) {
    const serviceIds = workItem.document.answers.edges
      .flatMap((edge) =>
        edge.node.value.map((doc) => parseInt(doc.createdByGroup))
      )
      .filter(Boolean);

    if (!serviceIds.length) {
      return;
    }

    return yield this.store.query("service", {
      service_id: serviceIds.join(","),
    });
  }
}
