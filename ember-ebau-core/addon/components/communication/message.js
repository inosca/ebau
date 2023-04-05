import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";

export default class CommunicationMessageComponent extends Component {
  @service store;
  @service notification;
  @service router;
  @service intl;
  @service session;

  @tracked collapsed = true;
  @tracked paragraph;

  get isExpandable() {
    return this.paragraph?.clientWidth < this.paragraph?.scrollWidth;
  }

  get readByEveryone() {
    const message = this.args.message;
    return (
      message.readByEntity.length ===
      message.topic.get("involvedEntities").length
    );
  }

  markAsRead = task(async () => {
    try {
      await this.args.message.markAsRead();
      await this.store.findRecord(
        "communications-message",
        this.args.message.id
      );
    } catch (error) {
      console.error(error);
      this.notification.danger(
        this.intl.t("communications.detail.markAsReadError")
      );
    }
  });

  markAsUnread = task(async () => {
    try {
      //TODO
      alert("Not yet implemented in api.");
    } catch (error) {
      console.error(error);
      this.notification.danger(
        this.intl.t("communications.detail.markAsUnreadError")
      );
    }
  });

  @action
  setParagraph(element) {
    this.paragraph = element;
  }

  @action
  toggleText(event) {
    event?.preventDefault();
    if (this.isExpandable || !this.collapsed) {
      this.collapsed = !this.collapsed;
    }
  }
}
