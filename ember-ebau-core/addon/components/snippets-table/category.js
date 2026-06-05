import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { confirm } from "ember-uikit";

export default class SnippetsTableCategory extends Component {
  @service intl;
  @service fetch;
  @service notification;

  @tracked isExpanded = true;
  @tracked isEditing = false;
  @tracked name = "";

  constructor(...args) {
    super(...args);

    this.name = this.args.category;
  }

  @action
  toggleExpanded(event) {
    event.preventDefault();

    this.isExpanded = !this.isExpanded;
  }

  @action
  toggleEditing(event) {
    event?.preventDefault();

    this.isEditing = !this.isEditing;

    if (!this.isEditing) {
      this.name = this.args.category;
    }
  }

  @action
  copySnippet(snippet, event) {
    event?.preventDefault();

    navigator.clipboard.writeText(snippet.body);
    this.notification.success(
      this.intl.t("snippets.success.copy", { name: snippet.subject }),
    );
  }

  save = dropTask(this, async (event) => {
    event.preventDefault();

    try {
      const response = await this.fetch.fetch(
        `/api/v1/notification-templates/update_purposes?current=${this.args.category}&new=${this.name}`,
        { method: "PATCH" },
      );

      if (!response.ok) {
        throw new Error();
      }

      this.notification.success(this.intl.t("snippets.success.save-category"));

      this.isEditing = false;
      this.args.refresh();
    } catch {
      this.notification.danger(this.intl.t("snippets.error.save-category"));
    }
  });

  deleteCategory = dropTask(this, async (event) => {
    event.preventDefault();

    if (
      !(await confirm(
        this.intl.t("snippets.confirm.delete-category", {
          name: this.name,
        }),
      ))
    ) {
      return;
    }

    try {
      const response = await this.fetch.fetch(
        `/api/v1/notification-templates/delete_by_purpose?purpose=${this.args.category}`,
        { method: "DELETE" },
      );

      if (!response.ok) {
        throw new Error();
      }

      this.notification.success(
        this.intl.t("snippets.success.delete-category"),
      );

      await this.args.refresh();
    } catch {
      this.notification.danger(this.intl.t("snippets.error.delete-category"));
    }
  });

  deleteSnippet = dropTask(this, async (snippet, event) => {
    event.preventDefault();

    if (
      !(await confirm(
        this.intl.t("snippets.confirm.delete", {
          name: snippet.subject,
        }),
      ))
    ) {
      return;
    }

    try {
      await snippet.destroyRecord();

      this.notification.success(this.intl.t("snippets.success.delete"));
    } catch {
      this.notification.danger(this.intl.t("snippets.error.delete"));
    }
  });
}
