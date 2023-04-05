import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { trackedFunction } from "ember-resources/util/function";

import { paginatedQuery } from "ember-ebau-core/resources/paginated";

export default class CommunicationTopicComponent extends Component {
  @service store;

  topic = trackedFunction(this, async () =>
    this.args.topic?.id
      ? this.args.topic
      : await this.store.findRecord("communications-topic", this.args.topic)
  );

  messages = paginatedQuery(this, "communications-message", () => ({
    topic: this.args.topic.id ?? this.args.topic,
    page: {
      number: this.page,
      size: 20,
    },
  }));
}
