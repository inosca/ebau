import { action } from "@ember/object";
import { later } from "@ember/runloop";
import { inject as service } from "@ember/service";
import { macroCondition, isTesting } from "@embroider/macros";
import Component from "@glimmer/component";

export default class NotificationsComponent extends Component {
  @service notification;

  @action
  remove(notification, event) {
    event?.preventDefault();

    this.notification.remove(notification.id);
  }

  @action
  scheduleRemoval(notification) {
    if (macroCondition(isTesting())) {
      // don't schedule removal in tests
    } else {
      later(this, "remove", notification, 5000);
    }
  }
}
