import Service from "@ember/service";
import { query } from "ember-data-resources";

export default class CommunicationsUnreadMessagesService extends Service {
  get count() {
    return this.unreadMessagesResource.records?.meta.pagination.count;
  }

  unreadMessagesResource = query(this, "communications-message", () => ({
    is_read: false,
    page: {
      number: 1,
      size: 1,
    },
  }));
}
