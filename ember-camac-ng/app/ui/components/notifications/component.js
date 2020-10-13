import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

const STYLES = ["camac", "uikit"];

export default class NotificationsComponent extends Component {
  @service notifications;

  get style() {
    const style = (this.args.style || STYLES[0]).toLowerCase();

    return STYLES.includes(style) ? style : STYLES[0];
  }

  @action
  remove(notification, event) {
    event.preventDefault();

    this.notifications.remove(notification.id);
  }
}
