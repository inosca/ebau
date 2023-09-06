import Service, { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";

export default class AlexandriaConfigService extends Service {
  @service store;
  @service session;

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

  namespace = "/alexandria/api/v1";
  zipDownloadNamespace = "/alexandria";
}
