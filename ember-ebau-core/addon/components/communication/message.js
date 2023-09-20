import { action } from "@ember/object";
import { scheduleOnce } from "@ember/runloop";
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

  @localCopy("args.collapsed", true) collapsed;
  @tracked paragraph;
  @tracked isTruncated;

  get isExpandable() {
    return (
      this.isTruncated ||
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
        this.intl.t("communications.detail.markAsReadError"),
      );
    }
  });

  markAsUnread = task(async () => {
    try {
      await this.args.message.markAsUnread();
    } catch (error) {
      console.error(error);
      this.notification.danger(
        this.intl.t("communications.detail.markAsUnreadError"),
      );
    }
  });

  @action
  setTruncated(paragraphElement) {
    if (!this.paragraph) {
      this.paragraph = paragraphElement;
    }

    this.isTruncated =
      paragraphElement?.clientWidth < paragraphElement?.scrollWidth;
  }

  @action
  toggleText(event) {
    event?.preventDefault();

    // Get the current text selection to prevent toggling while selecting text
    // from a message
    const selection = window.getSelection().toString();

    if (!selection.length && (this.isExpandable || !this.collapsed)) {
      this.collapsed = !this.collapsed;

      // Recalculate isTruncated property after rendering
      scheduleOnce("afterRender", this, "setTruncated", this.paragraph);
    }
  }
}
