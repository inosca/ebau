import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class BillingGlobalController extends Controller {
  queryParams = ["from", "to"];

  @tracked from = "";
  @tracked to = "";
  @tracked page = 1;

  entries = paginatedQuery(this, "billing-v2-entry", () => ({
    filter: {
      ...(this.from ? { dateAddedAfter: this.from } : {}),
      ...(this.to ? { dateAddedBefore: this.to } : {}),
    },
    page: {
      number: this.page,
      size: 20,
    },
    include: "user,group,group.service",
  }));

  @action
  loadMore() {
    this.page += 1;
  }

  @action
  updateFilter(name, { target: { value } }) {
    this.page = 1;
    this[name] = value;
  }
}
