import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { tracked } from "@glimmer/tracking";
import { inject as service } from "@ember/service";

export default class CommunicationMessageModel extends Model {
  @service store;
  @service session;

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
    const headers = {
      authorization: `Bearer ${this.session.data.authenticated?.access_token}`,
    };

    const response = await fetch(`${url}/${action}`, { method, headers, body });
    return response.ok;
  }

  async markAsRead() {
    return await this.apiAction("read");
  }
}
