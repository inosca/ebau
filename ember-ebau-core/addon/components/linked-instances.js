import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { gql } from "graphql-tag";

import CustomCaseModel from "ember-ebau-core/caluma-query/models/case";

export default class LinkedInstancesComponent extends Component {
  @queryManager apollo;

  @service fetch;
  @service intl;
  @service notification;
  @service store;
  @service ebauModules;

  @tracked dossierNumber;

  @dropTask
  *fetchCurrentInstance(reload = false) {
    return yield this.store.findRecord(
      "instance",
      this.args.currentInstance.id,
      {
        reload,
        include: "linked_instances",
      },
    );
  }

  @dropTask
  *searchAndLinkDossier() {
    try {
      const caseRecord = yield this.apollo.query(
        {
          query: gql`
            query GetCase($metaFilter: [JSONValueFilterType]) {
              allCases(filter: [{ metaValue: $metaFilter }]) {
                edges {
                  node {
                    ...CaseFragment
                  }
                }
              }
            }

            fragment CaseFragment on Case ${CustomCaseModel.fragment}
          `,
          variables: {
            metaFilter: [
              {
                key: "dossier-number",
                value: this.dossierNumber.trim(),
              },
            ],
          },
        },
        "allCases.edges",
      );
      const modelInstance = new CustomCaseModel(caseRecord?.[0]?.node);
      return yield this.linkDossier.perform(
        modelInstance.meta["camac-instance-id"],
      );
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("cases.miscellaneous.linkInstanceError"),
      );
    }
  }

  @dropTask
  *linkDossier(instanceId) {
    try {
      yield this.fetch.fetch(
        `/api/v1/instances/${this.args.currentInstance.id}/link`,
        {
          method: "PATCH",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            data: {
              attributes: {
                "link-to": instanceId,
              },
            },
          }),
        },
      );

      yield this.fetchCurrentInstance.perform(true);
      this.dossierNumber = null;
      this.notification.success(
        this.intl.t("cases.miscellaneous.linkInstanceSuccess"),
      );
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("cases.miscellaneous.linkInstanceError"),
      );
    }
  }

  @dropTask
  *unLinkDossier(instance) {
    try {
      yield instance.unlink();
      yield this.fetchCurrentInstance.perform();
      this.notification.success(
        this.intl.t("cases.miscellaneous.unLinkInstanceSuccess"),
      );
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("cases.miscellaneous.unLinkInstanceError"),
      );
    }
  }
}
