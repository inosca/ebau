import { assert } from "@ember/debug";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task, timeout } from "ember-concurrency";
import { queryRecord, findRecord } from "ember-data-resources";
import { trackedFunction } from "ember-resources/util/function";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class CommunicationTopicComponent extends Component {
  @service store;
  @service notification;
  @service router;
  @service intl;
  @service session;

  @tracked page = 1;

  get topicId() {
    return this.args.topic?.id ?? this.args.topic;
  }

  get newMessage() {
    return this.newMessageResource.value;
  }

  topicResource = findRecord(this, "communications-topic", () => [
    this.topicId,
    { include: "initiated_by" },
  ]);

  messagesResource = paginatedQuery(this, "communications-message", () => ({
    topic: this.topicId,
    page: {
      number: this.page,
      size: 20,
    },
    include: "created_by_user",
  }));

  newMessageResource = trackedFunction(this, async () => {
    const topic = this.topicResource.record;
    if (topic) {
      return this.store.createRecord("communications-message", {
        topic,
      });
    }
  });

  constructor(owner, args) {
    super(owner, args);
    assert(
      "Must specify argument @topic on <NewTopic/> component.",
      this.args.topic
    );
  }

  @action
  updateMessage(body) {
    this.newMessage.body = body;
  }

  @action
  updateFiles(files) {
    this.newMessage.filesToSave = files;
  }

  sendMessage = task(async () => {
    try {
      await this.newMessage.save();
      await this.messagesResource.retry();
      await this.newMessageResource.retry();
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("communications.new.saveError"));
    }
  });
}
