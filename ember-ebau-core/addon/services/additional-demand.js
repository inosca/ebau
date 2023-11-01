import { getOwner, setOwner } from "@ember/application";
import { action } from "@ember/object";
import Service, { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";

import CustomWorkItemModel from "ember-ebau-core/caluma-query/models/work-item";
import additionalDemandQuery from "ember-ebau-core/gql/queries/additional-demand/list.graphql";
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

      data.demands.edges.forEach((edge) => {
        const workItem = new CustomWorkItemModel(edge.node);
        setOwner(workItem, getOwner(this));

        if (!workItem.createdByGroup) {
          servicesToFetch.add(workItem.raw.createdByGroup);
        }
      });

      if (servicesToFetch.size) {
        await this.store.query(this.ebauModules.storeServiceName, {
          service_id: [...servicesToFetch].join(","),
        });
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
