import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class NotificationsComponent extends Component {
  @service notifications;

  @action
  remove(notification) {
    this.notifications.remove(notification.id);
  }
}
