import { action, get } from "@ember/object";
import { service } from "@ember/service";
import { getConfig } from "@embroider/macros";
import { tracked } from "@glimmer/tracking";
import AlexandriaConfigService from "ember-alexandria/services/alexandria-config";
import fetchIfNotCached from "ember-ebau-core/utils/fetch-if-not-cached";

const allowedWebDAVMimeTypes =
  getConfig("ember-ebau-core").allowedWebDAVMimeTypes;

export default class CustomAlexandriaConfigService extends AlexandriaConfigService {
  markIcons = {
    decision: "stamp",
    publication: "bullhorn",
    void: "ban",
    objection: "hand-point-up",
    sensitive: "triangle-exclamation",
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
  async resolveUser(id) {
    if (!id) return "-";

    await fetchIfNotCached("public-user", "id", [id], this.store);
    return this.store.peekRecord("public-user", id)?.fullName ?? "-";
  }

  @action
  async resolveGroup(id) {
    if (!id) return "-";

    await fetchIfNotCached("public-service", "id", [id], this.store);
    return this.store.peekRecord("public-service", id)?.name ?? "-";
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
        this.store.query("public-user", { filter: { id: users.join(",") } }),
      );
    }
    if (groups.length) {
      requests.push(
        await this.store.query("public-service", {
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
  allowedWebDAVMimeTypes = allowedWebDAVMimeTypes.split(",");
}
