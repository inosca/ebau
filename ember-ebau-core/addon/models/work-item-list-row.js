import { action } from "@ember/object";
import { service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Model, { attr, belongsTo } from "@ember-data/model";

export default class WorkItemListRowModel extends Model {
  @service fetch;
  @service ebauModules;

  @attr applicants;
  @attr closedAt;
  @attr deadline;
  @attr targetDeadlineDate;
  @attr description;
  @attr directLink;
  @attr editLink;
  @attr instanceId;
  @attr instanceName;
  @attr isAddressedToCurrentService;
  @attr isAssignedToCurrentUser;
  @attr isControlledByCurrentService;
  @attr isCreatedByCurrentService;
  @attr isManuallyCompletable;
  @attr isReady;
  @attr isSuspended;
  @attr municipality;
  @attr specialId;
  @attr status;
  @attr task;
  @attr unread;

  @belongsTo("public-service", { inverse: null, async: true, readOnly: true })
  addressedService;
  @belongsTo("public-user", { inverse: null, async: true, readOnly: true })
  assignedUser;
  @belongsTo("public-user", { inverse: null, async: true, readOnly: true })
  closedByUser;

  get link() {
    if (!this.isAddressedToCurrentService) {
      return this.editLink;
    }

    return this.directLink ?? this.editLink;
  }

  get instance() {
    return htmlSafe(
      `${this.instanceName} <span class="uk-text-nowrap">(${this.specialId})</span>`,
    );
  }

  get closedBy() {
    // eslint-disable-next-line ember/no-get, ember/classic-decorator-no-classic-methods
    return this.get("closedByUser.fullName");
  }

  get responsible() {
    // eslint-disable-next-line ember/no-get, ember/classic-decorator-no-classic-methods
    const user = this.get("assignedUser.fullName");

    if (this.isAddressedToCurrentService) {
      return user ?? "-";
    }

    return (
      // eslint-disable-next-line ember/no-get, ember/classic-decorator-no-classic-methods
      [this.get("addressedService.name"), user ? `(${user})` : null]
        .filter(Boolean)
        .join(" ") || "-"
    );
  }

  @action
  async toggleRead() {
    const response = await this.fetch.fetch(
      `/api/v1/work-item-list-rows/${this.id}/toggle-read`,
      { method: "POST" },
    );
    this.store.pushPayload(await response.json());
  }

  @action
  async assignToMe() {
    const response = await this.fetch.fetch(
      `/api/v1/work-item-list-rows/${this.id}/assign-to-me?include=assigned_user`,
      { method: "POST" },
    );
    this.store.pushPayload(await response.json());
  }

  @action
  async quickComplete() {
    const response = await this.fetch.fetch(
      `/api/v1/work-item-list-rows/${this.id}/quick-complete?include=closed_by_user`,
      { method: "POST" },
    );
    this.store.pushPayload(await response.json());
  }
}
