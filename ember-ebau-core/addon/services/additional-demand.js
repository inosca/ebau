import { getOwner, setOwner } from "@ember/application";
import { action } from "@ember/object";
import Service, { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";

import CustomWorkItemModel from "ember-ebau-core/caluma-query/models/work-item";
import additionalDemandQuery from "ember-ebau-core/gql/queries/additional-demand/list.graphql";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import apolloQuery from "ember-ebau-core/resources/apollo";

export default class EbauModulesService extends Service {
  @service store;
  @service ebauModules;

  @queryManager apollo;

  @tracked instanceId;

  _additionalDemands = apolloQuery(
    this,
    () => ({
      query: additionalDemandQuery,
      fetchPolicy: "network-only",
      variables: {
        instanceId: this.instanceId,
        group: String(this.ebauModules.serviceId),
      },
    }),
    null,
    async (data) => {
      const servicesToFetch = new Set();
      const usersToFetch = new Set();

      data.demands.edges.forEach((edge) => {
        const workItem = new CustomWorkItemModel(edge.node);
        setOwner(workItem, getOwner(this));

        if (hasFeature("additionalDemands.showAuthor")) {
          workItem.childCase.workItems.forEach((childWorkItem) => {
            if (childWorkItem.isCompleted) {
              if (!childWorkItem.closedByUser) {
                usersToFetch.add(childWorkItem.raw.closedByUser);
              }
              if (!childWorkItem.closedByGroup) {
                servicesToFetch.add(childWorkItem.raw.closedByGroup);
              }
            }
          });
        }

        if (!workItem.createdByGroup) {
          servicesToFetch.add(workItem.raw.createdByGroup);
        }

        if (!workItem.addressedService) {
          workItem.raw.addressedGroups.forEach((serviceId) =>
            servicesToFetch.add(serviceId),
          );
        }
      });

      const services = [...servicesToFetch].filter(Boolean);

      if (services.length) {
        await this.store.query(this.ebauModules.storeServiceName, {
          service_id: services.join(","),
        });
      }

      const users = [...usersToFetch].filter(Boolean);
      if (users.length) {
        await this.store.query("public-user", { username: users.join(",") });
      }

      return data;
    },
  );

  get additionalDemands() {
    const demands = this._additionalDemands.value?.demands.edges.map((edge) => {
      const workItem = new CustomWorkItemModel(edge.node);
      setOwner(workItem, getOwner(this));
      return workItem;
    });

    return {
      demands,
      init: this._additionalDemands.value?.init.edges[0]?.node,
    };
  }

  get demands() {
    return this.additionalDemands.demands ?? [];
  }

  get validAdditionalDemands() {
    return this.demands.filter((demand) => {
      // Due to migrated data the send-additional-demand work-item
      // may not appear in order, but there should only be one.
      const sendWorkItem = demand.raw.childCase.workItems.edges.find(
        ({ node }) => node.task.slug === "send-additional-demand",
      );

      return sendWorkItem?.node.status !== "CANCELED";
    });
  }

  get latestDemand() {
    return this.validAdditionalDemands?.at(-1);
  }

  get initWorkItem() {
    return this.additionalDemands.init;
  }

  get isRunning() {
    return this._additionalDemands.isLoading;
  }

  @action
  async refetch() {
    return this._additionalDemands.reload();
  }
}
