import Service from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { v4 } from "uuid";

/**
 * This service intentionally overrides the notification service of ember-uikit
 * and provides all the same functionality. This is needed because in
 * ember-camac-ng we need to render notifications inside the page - not as
 * overlay notification since the app is embedded.
 */
export default class NotificationService extends Service {
  @tracked all = [];

  add(type, message) {
    const id = v4();

    this.all = [...this.all, { id, type, message }];
  }

  remove(id) {
    this.all = this.all.filter((obj) => obj.id !== id);
  }

  clear() {
    this.all = [];
  }

  default(message) {
    this.add("default", message);
  }

  primary(message) {
    this.add("primary", message);
  }

  success(message) {
    this.add("success", message);
  }

  warning(message) {
    this.add("warning", message);
  }

  danger(message) {
    this.add("danger", message);
  }
}
