import { getOwner, setOwner } from "@ember/application";
import { A } from "@ember/array";
import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import getAudit from "camac-ng/gql/queries/get-audit.graphql";
import getEbauNumber from "camac-ng/gql/queries/get-ebau-number.graphql";
import Audit from "camac-ng/ui/audit/audit";

export default class AuditController extends Controller {
  @service store;
  @service notifications;
  @service intl;

  @queryManager apollo;

  get auditWorkItem() {
    return this.auditWorkItems?.find(
      (workItem) => workItem.caseData.instanceId === this.model
    );
  }

  get audits() {
    return A(
      this.auditWorkItem?.document.answers.edges.flatMap((edge) =>
        edge.node.value.map((raw) =>
          this.createAudit(raw, this.auditWorkItem.caseData)
        )
      )
    )
      .sortBy("type", "createdAt")
      .reverse();
  }

  get auditsWithSameEbauNumber() {
    const workItems = this.auditWorkItems?.filter(
      (workItem) => workItem.caseData.instanceId !== this.model
    );

    return workItems
      ?.map((workItem) => {
        return {
          instanceId: workItem.caseData.instanceId,
          form: workItem.caseData.form,
          audits: workItem.document.answers.edges.flatMap((edge) =>
            edge.node.value.map((raw) =>
              this.createAudit(raw, workItem.caseData)
            )
          ),
        };
      })
      .filter((auditGroup) => auditGroup.audits.length);
  }

  get documentData() {
    const document = this.auditWorkItem?.document;

    return (
      document && {
        id: decodeId(document.id),
        ...document.answers.edges.reduce((obj, { node }) => {
          return {
            ...obj,
            [node.question.rowForm.slug]: node.value.map((doc) =>
              decodeId(doc.id)
            ),
          };
        }, {}),
      }
    );
  }

  createAudit(rawDocument, caseData) {
    const audit = new Audit(rawDocument, caseData);

    setOwner(audit, getOwner(this));

    return audit;
  }

  @lastValue("fetchAudit") auditWorkItems;
  @dropTask
  *fetchAudit() {
    try {
      const ebauNumber = yield this.apollo.query(
        {
          query: getEbauNumber,
          fetchPolicy: "network-only",
          variables: { instanceId: this.model },
        },
        "allCases.edges.firstObject.node.meta.ebau-number"
      );

      const response = yield this.apollo.query({
        query: getAudit,
        fetchPolicy: "network-only",
        variables: { ebauNumber },
      });

      try {
        // populate work items with case data for later
        const workItems = response.allCases.edges.map((edge) => ({
          ...edge.node.workItems.edges[0].node,
          caseData: {
            instanceId: edge.node.meta["camac-instance-id"],
            form: edge.node.document.form.name,
          },
        }));

        yield this.fetchAdditionalData.perform(workItems);

        return workItems;
      } catch (error) {
        // no audit work item (migration)
        return null;
      }
    } catch (error) {
      this.notifications.error(this.intl.t("audit.loadingError"));
    }
  }

  @dropTask
  *fetchAdditionalData(workItems) {
    const cachedServiceIds = this.store
      .peekAll("service")
      .map((service) => parseInt(service.id, 10));
    const cachedUsernames = this.store
      .peekAll("public-user")
      .map((user) => user.username);

    const serviceIds = [
      ...new Set(
        workItems.flatMap((workItem) =>
          workItem.document.answers.edges
            .flatMap((edge) =>
              edge.node.value.map((doc) => [
                doc.createdByGroup,
                doc.modifiedContentByGroup,
              ])
            )
            .map((id) => parseInt(id, 10))
            .filter((id) => id && !cachedServiceIds.includes(id))
        )
      ),
    ];

    const usernames = [
      ...new Set(
        workItems.flatMap((workItem) =>
          workItem.document.answers.edges
            .flatMap((edge) =>
              edge.node.value.map((doc) => doc.modifiedContentByUser)
            )
            .filter(
              (username) => username && !cachedUsernames.includes(username)
            )
        )
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
