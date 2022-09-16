import Service from "@ember/service";
import { tracked } from "@glimmer/tracking";

export default class AlexandriaConfigService extends Service {
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

  resolveUser() {}
  resolveGroup() {}

  namespace = "/alexandria/api/v1";
}
