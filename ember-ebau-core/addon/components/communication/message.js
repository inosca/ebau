import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { localCopy } from "tracked-toolbox";

export default class CommunicationMessageComponent extends Component {
  @service store;
  @service notification;
  @service router;
  @service intl;

  @localCopy("args.collapsed", true) _collapsed;
  @tracked paragraph;

  get collapsed() {
    return !this.isExpandable || this._collapsed;
  }

  get isExpandable() {
    return (
      this.paragraph?.clientWidth < this.paragraph?.scrollWidth ||
      this.args.message.attachments.length ||
      /\r|\n/.test(this.args.message.body)
    );
  }

  get readByEveryone() {
    const message = this.args.message;
    return (
      message.readByEntity.length ===
      message.get("topic.involvedEntities.length")
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
      this._collapsed = !this.collapsed;
    }
  }
}
