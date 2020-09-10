import { later } from "@ember/runloop";
import Service from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { v4 } from "uuid";

import config from "camac-ng/config/environment";

const TIMEOUT = 10000;

export default class NotificationsService extends Service {
  @tracked all = [];

  add(type, message) {
    const id = v4();

    this.all = [...this.all, { id, type, message }];

    if (config.environment !== "test") {
      later(this, () => this.remove(id), TIMEOUT);
    }
  }

  remove(id) {
    this.all = this.all.filter(obj => obj.id !== id);
  }

  clear() {
    this.all = [];
  }

  success(message) {
    this.add("success", message);
  }

  error(message) {
    this.add("error", message);
  }
}
