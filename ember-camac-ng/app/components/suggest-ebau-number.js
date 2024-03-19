import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import getSourceCaseMeta from "ember-ebau-core/gql/queries/get-source-case-meta.graphql";
import { trackedTask } from "reactiveweb/ember-concurrency";

export default class SuggestEbauNumberComponent extends Component {
  @queryManager apollo;

  sourceMeta = trackedTask(this, this.fetchSourceMeta, () => [
    this.args.context.instanceId,
  ]);

  @dropTask
  *fetchSourceMeta() {
    const response = yield this.apollo.query(
      {
        query: getSourceCaseMeta,
        variables: { instanceId: this.args.context.instanceId },
      },
      "allCases.edges",
    );

    return response[0]?.node.document.source?.case.meta ?? null;
  }

  @dropTask
  *applyEbauNumber() {
    const existingEbauNrField = this.args.field.document.findField(
      "ebau-number-has-existing",
    );
    existingEbauNrField.answer.value = "ebau-number-has-existing-yes";
    yield existingEbauNrField.save.perform();

    const ebauNumberField = this.args.field.document.findField(
      "ebau-number-existing",
    );
    ebauNumberField.answer.value = this.sourceMeta.value["ebau-number"];
    yield ebauNumberField.save.perform();
  }
}
