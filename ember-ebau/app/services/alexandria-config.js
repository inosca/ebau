import Service, { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";

export default class AlexandriaConfigService extends Service {
  @service store;

  @tracked caseId;

  get modelMetaFilters() {
    return {
      document: [{ key: "camac-instance-id", value: this.caseId.toString() }],
    };
  }

  get defaultModelMeta() {
    return {
      document: { "camac-instance-id": this.caseId },
    };
  }

  resolveUser(id) {
    if (!id) return "-";

    return this.store.peekRecord("user", id)?.fullName ?? "-";
  }

  resolveGroup(id) {
    if (!id) return "-";

    return this.store.peekRecord("service", id)?.name ?? "-";
  }

  namespace = "/alexandria/api/v1";
}
