import { getOwner, setOwner } from "@ember/application";
import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { queryManager } from "ember-apollo-client";

import CustomWorkItemModel from "ember-ebau-core/caluma-query/models/work-item";
import allAddressWorkItemsQuery from "ember-ebau-core/gql/queries/address-assignment/all-work-items.graphql";
import apolloQuery from "ember-ebau-core/resources/apollo";

export default class AddressAssignmentController extends Controller {
  @service("store") store;
  @queryManager apollo;
  @service ebauModules;

  get workItems() {
    return this._workItems.value ?? [];
  }

  _workItems = apolloQuery(
    this,
    () => ({
      query: allAddressWorkItemsQuery,
      fetchPolicy: "network-only",
      variables: {
        instanceId: this.ebauModules.instanceId,
      },
    }),
    null,
    async (data) => {
      const servicesToFetch = new Set();

      const workItems = data.allWorkItems.edges.map((edge) => {
        const workItem = new CustomWorkItemModel(edge.node);
        setOwner(workItem, getOwner(this));

        if (!workItem.createdByGroup) {
          servicesToFetch.add(workItem.raw.createdByGroup);
        }

        return workItem;
      });

      if (servicesToFetch.size) {
        await this.store.query(this.ebauModules.storeServiceName, {
          service_id: [...servicesToFetch].join(","),
        });
      }

      return workItems;
    },
  );

  @action
  onSuccess() {
    return this._workItems.reload();
  }
}
