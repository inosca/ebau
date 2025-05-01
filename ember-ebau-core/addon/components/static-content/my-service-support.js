import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { findRecord, query } from "ember-data-resources";

const LIMIT = 10;

export default class StaticContentMyServiceSupportComponent extends Component {
  @service ebauModules;

  @tracked page = 1;
  @tracked limit = LIMIT;

  service = findRecord(this, "service", () => this.ebauModules.serviceId);

  users = query(this, "user", () => ({
    admin_for_service: this.ebauModules.serviceId,
    "page[size]": this.limit,
    "page[number]": this.page,
  }));

  get hasMore() {
    return (
      this.users.records?.meta?.pagination?.count > this.users.records?.length
    );
  }

  get hasLess() {
    return this.users.records?.length > LIMIT;
  }

  @action
  toggle(event) {
    event.preventDefault();

    if (this.hasMore) {
      this.limit = null;
    } else if (this.hasLess) {
      this.limit = LIMIT;
    }
  }
}
