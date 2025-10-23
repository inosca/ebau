import Route from "@ember/routing/route";
import { service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import mainConfig from "ember-ebau-core/config/main";
import getCaseBySpecialId from "ember-ebau-core/gql/queries/get-case-by-special-id.graphql";

export default class InstancesEditRoute extends Route {
  @queryManager apollo;

  @service alexandriaConfig;
  @service ebauModules;
  @service permissions;
  @service store;
  @service router;

  async model({ instance }) {
    if (instance.includes("-")) {
      // try to find instance by "special" id (dossier number)
      const instanceId = await this.apollo.query(
        {
          query: getCaseBySpecialId,
          variables: {
            key: mainConfig.answerSlugs.specialId,
            value: instance,
          },
        },
        "allCases.edges.0.node.meta.camac-instance-id",
      );

      if (instanceId) {
        return this.router.replaceWith("instances.edit", instanceId);
      }
    } else {
      return parseInt(instance);
    }
  }

  async afterModel(instanceId) {
    this.alexandriaConfig.instanceId = instanceId;
    this.ebauModules.instanceId = instanceId;

    if (this.permissions.fullyEnabled) {
      await this.permissions.populateCacheFor(instanceId);
    }
  }

  setupController(controller, ...args) {
    super.setupController(controller, ...args);

    this.ebauModules.onAdditionalDemandComplete =
      controller.additionalDemandsCount.reload;

    controller.reload();
  }
}
