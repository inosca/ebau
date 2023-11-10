import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dedupeTracked } from "tracked-toolbox";

import { AVAILABLE_GRANT_TYPES } from "ember-ebau-core/models/instance-acl";
import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class AclTable extends Component {
  @service store;

  @dedupeTracked statusFilter = "all";
  @dedupeTracked accessLevelFilter = "";
  @dedupeTracked page = 1;

  @tracked detailViewAcl;

  availableGrantTypes = AVAILABLE_GRANT_TYPES;
  availableStatusFilterTypes = ["all", "active", "inactive"];

  get availableAccessLevels() {
    return this.store.findAll("access-level");
  }

  acls = paginatedQuery(this, "instance-acl", () => ({
    instance: this.args.instanceId,
    // TODO: include: "user", maybe in the future?
    filter: {
      status: this.statusFilter === "all" ? "" : this.statusFilter,
      accessLevel: this.accessLevelFilter?.slug,
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
}
