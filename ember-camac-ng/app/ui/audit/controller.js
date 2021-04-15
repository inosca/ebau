import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import getAudit from "camac-ng/gql/queries/get-audit";

export default class AuditController extends Controller {
  @service store;
  @service shoebox;
  @service notifications;
  @service intl;

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

      try {
        const workItem =
          response.allCases.edges[0].node.workItems.edges[0].node;

        yield this.fetchAdditionalData.perform(workItem);

        return workItem;
      } catch (error) {
        // no audit work item (migration)
        return null;
      }
    } catch (error) {
      this.notifications.error(this.intl.t("audit.loadingError"));
    }
  }

  @dropTask
  *fetchAdditionalData(workItem) {
    const cachedServiceIds = this.store
      .peekAll("service")
      .map((service) => parseInt(service.id, 10));
    const cachedUsernames = this.store
      .peekAll("public-user")
      .map((user) => user.username);

    const serviceIds = [
      ...new Set(
        workItem.document.answers.edges
          .flatMap((edge) =>
            edge.node.value.map((doc) => [
              doc.createdByGroup,
              doc.modifiedContentByGroup,
            ])
          )
          .map((id) => parseInt(id, 10))
          .filter((id) => id && !cachedServiceIds.includes(id))
      ),
    ];

    const usernames = [
      ...new Set(
        workItem.document.answers.edges
          .flatMap((edge) =>
            edge.node.value.map((doc) => doc.modifiedContentByUser)
          )
          .filter((username) => username && !cachedUsernames.includes(username))
      ),
    ];

    if (serviceIds.length) {
      yield this.store.query("service", {
        service_id: serviceIds.join(","),
      });
    }

    if (usernames.length) {
      yield this.store.query("public-user", {
        username: usernames.join(","),
      });
    }
  }
}
