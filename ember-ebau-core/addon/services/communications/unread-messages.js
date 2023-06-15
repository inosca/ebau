import Service, { inject as service } from "@ember/service";
import { tracked } from "tracked-built-ins";

export default class CommunicationsUnreadMessagesService extends Service {
  @service store;

  counts = tracked({});

  async fetchUnreadCount(instanceId) {
    await Promise.resolve();

    const response = await this.store.query("communications-message", {
      is_read: false,
      page: {
        number: 1,
        size: 1,
      },
      ...(instanceId ? { instance: instanceId } : {}),
    });

    const count = response.meta.pagination.count;

    this.counts[instanceId ?? "all"] = count;
  }

  async refreshForInstance(instanceId) {
    await this.fetchUnreadCount();
    await this.fetchUnreadCount(instanceId);
  }
}
