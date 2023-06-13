import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class CommunicationUnreadMessageBadgeComponent extends Component {
  @service("communications/unread-messages") unreadMessages;

  constructor(...args) {
    super(...args);

    this.unreadMessages.fetchUnreadCount(this.args.instanceId);
  }

  get count() {
    return this.unreadMessages.counts[this.args.instanceId ?? "all"];
  }
}
