import Service from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { v4 } from "uuid";

export default class NotificationsService extends Service {
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

  success(message) {
    this.add("success", message);
  }

  error(message) {
    this.add("error", message);
  }
}
