import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { findRecord, findAll } from "ember-data-resources";
import { dedupeTracked } from "tracked-toolbox";
import { confirm } from "ember-uikit";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class AclTable extends Component {
  @service store;
  @service intl;
  @service notification;

  @dedupeTracked statusFilter = "all";
  @dedupeTracked accessLevelFilter = "";
  @tracked page = 1;

  @tracked detailViewAcl;
  @tracked creatingAcl;

  get statusFilterOptions() {
    return [
      { value: "all", label: this.intl.t("permissions.status.all") },
      { value: "active", label: this.intl.t("permissions.status.active") },
      {
        value: "scheduled",
        label: this.intl.t("permissions.status.scheduled"),
      },
      { value: "expired", label: this.intl.t("permissions.status.expired") },
    ];
  }

  availableAccessLevels = findAll(this, "access-level", () => [
    this.args.instanceId,
  ]);
  instance = findRecord(this, "instance", () => [this.args.instanceId]);

  acls = paginatedQuery(this, "instance-acl", () => ({
    instance: this.args.instanceId,
    // TODO: include: "user", maybe in the future?
    filter: {
      ...(this.statusFilter === "all" ? {} : { status: this.statusFilter }),
      ...(this.accessLevelFilter
        ? { accessLevel: this.accessLevelFilter.slug }
        : {}),
    },
    page: {
      number: this.page,
      size: 20,
    },
  }));

  @action
  updateStatusFilter(_, value) {
    this.statusFilter = value;
    this.page = 1;
  }

  @action
  updateAccessLevelFilter(value) {
    this.accessLevelFilter = value;
    this.page = 1;
  }

  @action
  updatePage() {
    if (this.acls.hasMore && !this.acls.isLoading) {
      this.page += 1;
    }
  }

  @action
  reload() {
    this.acls.retry();
  }

  @action
  async revokeAcl(acl) {
    try {
      await confirm(this.intl.t("permissions.confirmRevoke"));
      await acl.revoke();
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("permissions.revokeError"));
    }
  }
}
