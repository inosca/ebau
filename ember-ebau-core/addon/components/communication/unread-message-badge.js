import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class CommunicationUnreadMessageBadgeComponent extends Component {
  @service("communications/unread-messages") unreadMessages;
}
