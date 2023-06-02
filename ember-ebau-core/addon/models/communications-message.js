import { inject as service } from "@ember/service";
import Model, { attr, belongsTo } from "@ember-data/model";
import { tracked } from "@glimmer/tracking";

export default class CommunicationMessageModel extends Model {
  @service store;
  @service("communications/unread-messages") unreadMessages;
  @service fetch;

  @attr body;
  @attr createdAt;
  @attr createdBy;
  @attr readAt;
  @attr readByEntity;

  @belongsTo("communications-topic") topic;
  @belongsTo("user") createdByUser;

  // For temporary handling of files in the creation process
  @tracked filesToSave = [];

  async apiAction(action, method = "PATCH") {
    const modelName = "communications-message";
    const adapter = this.store.adapterFor(modelName);

    const url = adapter.buildURL(modelName, this.id);
    const body = JSON.stringify(adapter.serialize(this));

    const response = await this.fetch.fetch(`${url}/${action}`, {
      method,
      body,
    });
    const json = await response.json();
    this.store.pushPayload(json);
  }

  async markAsRead() {
    return await this.apiAction("read");
  }

  async markAsUnread() {
    const response = await this.apiAction("unread");
    await this.unreadMessages.unreadMessagesResource.retry();
    return response;
  }
}
