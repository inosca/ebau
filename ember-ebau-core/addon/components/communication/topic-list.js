import { assert } from "@ember/debug";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { query } from "ember-data-resources";

export default class CommunicationTopicListComponent extends Component {
  @service router;

  @tracked showOnlyUnread = false;

  topics = query(this, "communications-topic", () => ({
    has_unread: this.showOnlyUnread,
    instance: this.args.instance,
    include: "instance,involved_entities",
  }));

  constructor(owner, args) {
    super(owner, args);
    assert(
      "Must specify argument @detailRoute on <TopicList/> component.",
      typeof args.detailRoute === "string"
    );
    if (args.instance) {
      assert(
        "Must specify argument @newRoute on <TopicList/> component.",
        typeof args.newRoute === "string"
      );
    }
  }

  @action
  transitionToTopic(instanceId) {
    this.router.transitionTo(this.args.detailRoute, instanceId);
  }
}
