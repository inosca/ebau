import Service, { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";

export default class AlexandriaConfigService extends Service {
  @service store;

  @tracked caseId;

  get modelMetaFilters() {
    return {
      document: [{ key: "case_id", value: this.caseId }],
    };
  }
  get defaultModelMeta() {
    return {
      document: { case_id: this.caseId },
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
