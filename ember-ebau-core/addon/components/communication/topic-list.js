import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { query } from "ember-data-resources";

export default class CommunicationTopicListComponent extends Component {
  @tracked showOnlyUnread = false;

  topics = query(this, "communications-topic", () => ({
    unread: this.showOnlyUnread,
    included: "instance,involved_entities",
  }));
}
