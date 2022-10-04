import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class NotificationsComponent extends Component {
  @service notification;

  @action
  remove(notification, event) {
    event.preventDefault();

    this.notification.remove(notification.id);
  }
}
