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

  @tracked collapsed = true;
  @tracked paragraph;

  get isExpandable() {
    return this.paragraph?.clientWidth < this.paragraph?.scrollWidth;
  }

  get readByEveryone() {
    const message = this.args.message;
    return (
      message.readByEntity.length ===
      message.topic?.get("involvedEntities").length
    );
  }

  markAsRead = task(async () => {
    try {
      await this.args.message.markAsRead();
      await this.args.refresh();
    } catch (error) {
      console.error(error);
      this.notification.danger(
        this.intl.t("communications.detail.markAsReadError")
      );
    }
  });

  markAsUnread = task(async () => {
    try {
      await this.args.message.markAsUnread();
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
