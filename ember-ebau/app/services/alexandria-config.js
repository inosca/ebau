import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import ConfigService from "ember-alexandria/services/config";

export default class AlexandriaConfigService extends ConfigService {
  markIcons = {
    decision: "stamp",
    publication: "bullhorn",
    void: "ban",
  };

  @service store;
  @service session;
  @service intl;

  @tracked instanceId;

  get modelMetaFilters() {
    return {
      document: [{ key: "camac-instance-id", value: String(this.instanceId) }],
    };
  }

  get defaultModelMeta() {
    return {
      document: { "camac-instance-id": String(this.instanceId) },
    };
  }

  get activeGroup() {
    return this.session.service.id;
  }
  set activeGroup(_) {
    // we do not need the setter
  }

  get activeUser() {
    return this.session.user.id;
  }

  get accessToken() {
    return this.session.data.authenticated.access_token;
  }

  resolveUser(id) {
    if (!id) return "-";

    return this.store.peekRecord("user", id)?.fullName ?? "-";
  }

  resolveGroup(id) {
    if (!id) return "-";

    return this.store.peekRecord("service", id)?.name ?? "-";
  }

  extractCreatedBy(documents, key) {
    return [...new Set(documents.map((d) => d[key]).filter((id) => id))];
  }

  documentsPostProcess(documents) {
    const users = this.extractCreatedBy(documents, "createdByUser");
    const groups = this.extractCreatedBy(documents, "createdByGroup");

    if (users.length) {
      this.store.query("user", { filter: { id: users.join(",") } });
    }
    if (groups.length) {
      this.store.query("service", { filter: { service_id: groups.join(",") } });
    }

    return documents;
  }

  namespace = "/alexandria/api/v1";
  zipDownloadNamespace = "/alexandria";
}
