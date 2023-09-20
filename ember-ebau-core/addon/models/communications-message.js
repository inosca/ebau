import { inject as service } from "@ember/service";
import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
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
  @hasMany("communications-attachment") attachments;

  // For temporary handling of files in the creation process
  @tracked filesToSave = [];
  @tracked documentAttachmentsToSave = [];

  async send() {
    const formData = new FormData();
    const { body, topic } = this;
    formData.append("body", body);
    formData.append(
      "topic",
      JSON.stringify({ id: topic.get("id"), type: "communications-topics" }),
    );
    this.filesToSave.forEach((file) => {
      formData.append("attachments", file);
    });
    this.documentAttachmentsToSave.forEach((documentAttachment) => {
      formData.append(
        "attachments",
        JSON.stringify({ id: documentAttachment }),
      );
    });
    await this.fetch.fetch("/api/v1/communications-messages", {
      method: "POST",
      body: formData,
      // Reset the content-type as specified in the FormData documentation on MDN:
      // Warning: When using FormData to submit POST requests using XMLHttpRequest or the Fetch_API with the multipart/form-data Content-Type (e.g. when uploading Files and Blobs to the server), do not explicitly set the Content-Type header on the request. Doing so will prevent the browser from being able to set the Content-Type header with the boundary expression it will use to delimit form fields in the request body.
      //  https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
      headers: {
        "content-type": null,
      },
    });
  }

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
    const response = await this.apiAction("read");
    await this.unreadMessages.refreshForInstance(this.topic.get("instance.id"));
    return response;
  }

  async markAsUnread() {
    const response = await this.apiAction("unread");
    await this.unreadMessages.refreshForInstance(this.topic.get("instance.id"));
    return response;
  }
}
