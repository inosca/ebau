import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class SanctionTemplatesNewRoute extends Route {
  @service store;
  @service ebauModules;

  model() {
    const service = this.store.peekRecord(
      "service",
      this.ebauModules.serviceId,
    );
    return this.store.createRecord("sanctionTemplate", {
      createdByService: service,
    });
  }
}
