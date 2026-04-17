import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class ApplicantConfirmationRound extends Ability {
  @service permissions;

  get #instanceId() {
    return this.model?.belongsTo("instance").id() ?? this.instanceId;
  }

  async #hasPermission(permission) {
    return await this.permissions.hasAll(
      this.#instanceId,
      `applicant-confirmation-${permission}`,
    );
  }

  async canStart() {
    return !this.model?.isActive && (await this.#hasPermission("start"));
  }

  async canConfirm() {
    return (
      this.model?.currentUserConfirmation?.status === "pending" &&
      (await this.#hasPermission("confirm"))
    );
  }

  async canCancel() {
    return (
      this.model.status === "running" && (await this.#hasPermission("cancel"))
    );
  }

  async canInvalidate() {
    return (
      this.model.status === "completed" &&
      (await this.#hasPermission("invalidate"))
    );
  }
}
