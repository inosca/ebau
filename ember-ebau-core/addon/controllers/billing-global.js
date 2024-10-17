import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { trackedFunction } from "reactiveweb/function";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class BillingGlobalController extends Controller {
  queryParams = ["from", "to", "serviceId"];

  @service store;

  @tracked from = "";
  @tracked to = "";
  @tracked page = 1;
  @tracked serviceId = "";

  entries = paginatedQuery(this, "billing-v2-entry", () => ({
    filter: {
      ...(this.from ? { dateAddedAfter: this.from } : {}),
      ...(this.to ? { dateAddedBefore: this.to } : {}),
      ...(this.serviceId ? { service: this.serviceId } : {}),
    },
    page: {
      number: this.page,
      size: 20,
    },
    include: "user,group,group.service",
  }));

  services = trackedFunction(this, async () => {
    const services = await this.store.query("public-service", {
      has_billing_entries: true,
    });

    return services.map((service) => ({
      label: service.name,
      value: service.id,
    }));
  });

  get selectedService() {
    return this.services.value?.find(
      (service) => service.value === this.serviceId,
    );
  }

  @action
  loadMore() {
    this.page += 1;
  }

  @action
  updateFilter(name, { target: { value } }) {
    this.page = 1;
    this[name] = value;
  }

  @action
  updateSelectFilter(name, value) {
    this.page = 1;
    this[name] = value?.value;
  }
}
