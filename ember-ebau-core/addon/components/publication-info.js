import { getOwnConfig } from "@embroider/macros";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import municipality from "ember-ebau-core/gql/queries/municipality.graphql";

export default class PublicationInfoComponent extends Component {
  @queryManager apollo;

  publicInstancesLink = trackedTask(this, this.getPublicInstancesLink, () => [
    this.args.instanceId,
  ]);

  @dropTask
  *getPublicInstancesLink() {
    try {
      const response = yield this.apollo.query(
        {
          query: municipality,
          variables: { instanceId: this.args.instanceId },
        },
        "allCases.edges",
      );

      const id = response[0].node.document.answers.edges[0].node.value;
      const portalURL = getOwnConfig().portalUrl;

      return `${portalURL}/public-instances?municipality=${id}`;
    } catch (e) {
      return null;
    }
  }
}
