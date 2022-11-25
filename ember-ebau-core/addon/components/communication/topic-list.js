import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { query } from "ember-data-resources";

export default class CommunicationTopicListComponent extends Component {
  @tracked showOnlyUnread = false;

  topics = query(this, "communications-topic", () => ({
    has_unread: this.showOnlyUnread,
    instance: this.args.instance,
    include: "instance,involved_entities",
  }));
}
