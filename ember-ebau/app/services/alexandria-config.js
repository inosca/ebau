import { action, get } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import AlexandriaConfigService from "ember-alexandria/services/alexandria-config";

export default class CustomAlexandriaConfigService extends AlexandriaConfigService {
  markIcons = {
    decision: "stamp",
    publication: "bullhorn",
    void: "ban",
    objection: "hand-point-up",
  };

  @service store;
  @service session;
  @service intl;
  @service router;

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

  @action
  resolveUser(id) {
    if (!id) return "-";

    return this.store.peekRecord("user", id)?.fullName ?? "-";
  }

  @action
  resolveGroup(id) {
    if (!id) return "-";

    return this.store.peekRecord("service", id)?.name ?? "-";
  }

  extractDocumentProperties(documents, key) {
    return [...new Set(documents.map((d) => get(d, key)))].filter((id) => id);
  }

  async documentsPostProcess(documents) {
    const users = this.extractDocumentProperties(documents, "createdByUser");
    const groups = this.extractDocumentProperties(documents, "createdByGroup");
    const instances = this.extractDocumentProperties(
      documents,
      "metainfo.camac-instance-id",
    );

    const requests = [];
    if (users.length) {
      requests.push(
        this.store.query("user", { filter: { id: users.join(",") } }),
      );
    }
    if (groups.length) {
      requests.push(
        await this.store.query("service", {
          filter: { service_id: groups.join(",") },
        }),
      );
    }
    if (instances.length) {
      requests.push(
        await this.store.query("instance", {
          filter: { instance_id: instances.join(",") },
        }),
      );
    }

    await Promise.all(requests);

    return documents;
  }

  @action
  documentListLinkTo(document) {
    const instance = this.store.peekRecord(
      "instance",
      document.metainfo["camac-instance-id"],
    );

    return {
      url: this.router.urlFor("cases.detail.alexandria", instance, {
        queryParams: {
          document: document.id,
        },
      }),
      label: instance.dossierNumber,
    };
  }

  namespace = "/alexandria/api/v1";
  zipDownloadNamespace = "/alexandria";
  enablePDFConversion = true;
  enableWebDAV = true;
}
