import { action } from "@ember/object";
import Service from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { v4 } from "uuid";

class Notification {
  @tracked showTechnicalInfo;

  constructor(id, type, message, options) {
    this.id = id;
    this.type = type;
    this.message = message;
    this.options = options;
  }

  @action
  toggleTechnicalInfo() {
    this.showTechnicalInfo = !this.showTechnicalInfo;
  }
}

/**
 * This service intentionally overrides the notification service of ember-uikit
 * and provides all the same functionality. This is needed because in
 * ember-camac-ng we need to render notifications inside the page - not as
 * overlay notification since the app is embedded.
 */
export default class NotificationService extends Service {
  @tracked all = [];

  add(type, message, options = {}) {
    const id = v4();

    this.all = [...this.all, new Notification(id, type, message, options)];
  }

  remove(id) {
    this.all = this.all.filter((obj) => obj.id !== id);
  }

  clear() {
    this.all = [];
  }

  default(message, options) {
    this.add("default", message, options);
  }

  primary(message, options) {
    this.add("primary", message, options);
  }

  success(message, options) {
    this.add("success", message, options);
  }

  warning(message, options) {
    this.add("warning", message, options);
  }

  danger(message, options) {
    this.add("danger", message, options);
  }
}
