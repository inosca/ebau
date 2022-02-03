import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";

import municipality from "camac-ng/gql/queries/municipality.graphql";

export default class PublicationInfoComponent extends Component {
  @service shoebox;

  @queryManager apollo;

  publicInstancesLink = useTask(this, this.getPublicInstancesLink, () => [
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
        "allCases.edges"
      );

      const id = response[0].node.document.answers.edges[0].node.value;
      const host = this.shoebox.content?.config?.portalURL;

      return `${host}/public-instances?municipality=${id}`;
    } catch (e) {
      return null;
    }
  }
}
