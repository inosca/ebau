import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { didCancel } from "ember-concurrency";
import { query } from "ember-data-resources";
import { confirm } from "ember-uikit";

import parseError from "ember-ebau-core/utils/parse-error";

export default class DeadlinesSuspensionListComponent extends Component {
  @service abilities;
  @service ebauModules;
  @service store;
  @service notification;
  @service intl;

  @tracked suspensionToEdit = undefined;
  @tracked showModal = false;

  suspensionsQuery = query(this, "suspension", () => ({
    filter: {
      deadline: this.args.deadline.id,
    },
    include: "deadline",
  }));

  get isLoading() {
    return this.suspensionsQuery.isLoading;
  }

  get suspensions() {
    return this.suspensionsQuery.records ?? [];
  }

  @action
  reload() {
    this.suspensionsQuery.retry();
    if (this.args.afterSave) {
      this.args.afterSave();
    }

    // reload instance for case header updates
    this.store.findRecord("instance", this.args.deadline.instance.id);
  }

  @action
  async createSuspension() {
    if (!(await this.abilities.can("create suspension"))) {
      return;
    }

    this.suspensionToEdit = undefined;
    this.showModal = true;
  }

  @action
  async editSuspension(suspension) {
    if (!(await this.abilities.can("edit suspension"))) {
      return;
    }

    this.suspensionToEdit = suspension;
    this.showModal = true;
  }

  @action
  async onDelete() {
    try {
      this.showModal = false;
      if (!(await confirm(this.intl.t("deadlines.suspension.confirmDelete")))) {
        this.suspensionToEdit = undefined;
        return;
      }

      await this.suspensionToEdit.destroyRecord();
      this.suspensionToEdit = undefined;
      this.notification.success(
        this.intl.t("deadlines.suspension.deleteSuccess"),
      );

      return this.reload();
    } catch (error) {
      if (didCancel(error)) {
        return;
      }

      this.notification.danger(
        parseError(error) || this.intl.t("deadlines.suspension.saveError"),
      );
      this.suspensionToEdit = undefined;
    }
  }
}
