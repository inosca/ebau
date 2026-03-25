import Route from "@ember/routing/route";
import { service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import mainConfig from "ember-ebau-core/config/main";
import getCaseBySpecialId from "ember-ebau-core/gql/queries/get-case-by-special-id.graphql";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class CasesDetailRoute extends Route {
  @queryManager apollo;

  @service alexandriaConfig;
  @service ebauModules;
  @service store;
  @service router;
  @service permissions;

  async model({ instance_id }) {
    if (instance_id.includes("-")) {
      // try to find instance by "special" id (dossier number)
      const instanceId = await this.apollo.query(
        {
          query: getCaseBySpecialId,
          variables: {
            key: mainConfig.answerSlugs.specialId,
            value: instance_id,
          },
        },
        "allCases.edges.0.node.meta.camac-instance-id",
      );

      if (instanceId) {
        return this.router.replaceWith("cases.detail", instanceId);
      }
    }
    this.alexandriaConfig.instanceId = parseInt(instance_id);
    this.ebauModules.instanceId = parseInt(instance_id);

    try {
      // fetch instance to allow reloading after state changes
      // from ebau-modules.js (redirectToCaseWorkItems)
      const includes = [
        "instance_state",
        "responsible_service_users",
        "linked_instances",
        "keywords",
        "static_keywords",
      ];
      if (hasFeature("instanceMarks")) {
        includes.push("instance_marks");
      }
      if (hasFeature("cases.showNoApplicantRegisteredWarning")) {
        includes.push("involved_applicants", "involved_applicants.invitee");
      }
      return await this.store.findRecord("instance", instance_id, {
        include: includes.join(","),
      });
    } catch (error) {
      console.error(error);
      this.router.transitionTo("cases.not-found");
    }
  }

  async afterModel() {
    if (this.permissions.fullyEnabled) {
      await this.permissions.populateCacheFor(this.ebauModules.instanceId);
    }
  }
}
