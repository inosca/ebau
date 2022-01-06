import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency-decorators";
import { useTask } from "ember-resources";

import getSourceCaseMeta from "camac-ng/gql/queries/get-source-case-meta.graphql";

export default class SuggestEbauNumberComponent extends Component {
  @queryManager apollo;

  sourceMeta = useTask(this, this.fetchSourceMeta, () => [
    this.args.context.instanceId,
  ]);

  @dropTask
  *fetchSourceMeta() {
    const response = yield this.apollo.query(
      {
        query: getSourceCaseMeta,
        variables: { instanceId: this.args.context.instanceId },
      },
      "allCases.edges"
    );

    return response[0]?.node.document.source?.case.meta ?? null;
  }

  @dropTask
  *applyEbauNumber() {
    const existingEbauNrField = this.args.field.document.findField(
      "besteht-bereits-eine-ebau-nummer"
    );
    existingEbauNrField.answer.value = "besteht-bereits-eine-ebau-nummer-ja";
    yield existingEbauNrField.save.perform();

    const ebauNumberField = this.args.field.document.findField(
      "bestehende-ebau-nummer"
    );
    ebauNumberField.answer.value = this.sourceMeta.value["ebau-number"];
    yield ebauNumberField.save.perform();
  }
}
