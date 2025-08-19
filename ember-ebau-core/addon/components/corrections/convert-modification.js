import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";

import getConstructionDescriptionQuery from "ember-ebau-core/gql/queries/get-construction-description.graphql";

export default class CorrectionsConvertModification extends Component {
  @queryManager apollo;

  @service fetch;
  @service notification;
  @service intl;

  @tracked showModal = false;
  @tracked constructionDescription;

  @action
  toggleModal() {
    this.showModal = !this.showModal;
  }

  @dropTask
  *editConstructionDescription() {
    try {
      yield this.fetch.fetch(
        `/api/v1/instances/${this.args.instance.id}/convert-modification`,
        {
          method: "PATCH",
          body: JSON.stringify({
            data: {
              type: "instance-convert-modifications",
              id: this.args.instance.id,
              attributes: {
                content: this.constructionDescription,
              },
            },
          }),
        },
      );
      this.toggleModal();

      // sadly we need this to have current data on the whole page
      location.reload();
    } catch {
      this.notification.danger(
        this.intl.t("corrections.modification-to-new-dossier.conversion-error"),
      );
    }
  }

  @dropTask
  *fetchConstructionDescription() {
    this.toggleModal();

    const response = yield this.apollo.query(
      {
        query: getConstructionDescriptionQuery,
        variables: { instanceId: this.args.instance.id },
      },
      "allCases.edges",
    );

    const answers = response[0].node.document.answers.edges.map(
      (edge) => edge.node.value,
    );

    this.constructionDescription = answers.join("\r\n");
  }
}
