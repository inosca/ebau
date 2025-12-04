import { action, get } from "@ember/object";
import { service } from "@ember/service";
import { getOwnConfig, macroCondition } from "@embroider/macros";
import { tracked } from "@glimmer/tracking";
import AlexandriaConfigService from "ember-alexandria/services/alexandria-config";

import fetchIfNotCached from "ember-ebau-core/utils/fetch-if-not-cached";

const allowedWebDAVMimeTypes = () => {
  const conf = getOwnConfig().allowedWebDAVMimeTypes;
  return (conf ?? "").split(",");
};
const enableOriginalDocumentFilename =
  getOwnConfig().enableAlexandriaOriginalDocumentFilename;

export default class CustomAlexandriaConfigService extends AlexandriaConfigService {
  markIcons = {
    decision: "stamp",
    publication: "bullhorn",
    void: "ban",
    objection: "hand-point-up",
    sensitive: "triangle-exclamation",
    geometer: "compass-drafting",
  };

  @service store;
  @service session;
  @service intl;
  @service router;
  @service ebauModules;

  @tracked instanceId;
  @tracked documentId;

  get modelMetaFilters() {
    return {
      document: [{ key: "camac-instance-id", value: String(this.instanceId) }],
    };
  }

  get categoryQueryParameters() {
    const params = {};
    if (macroCondition(getOwnConfig().application === "gr")) {
      if (this.instanceId) {
        params["camac-instance-id"] = String(this.instanceId);
      }
    }

    return params;
  }

  get defaultModelMeta() {
    return {
      document: {
        "camac-instance-id": String(this.instanceId),
        "caluma-document-id": this.documentId,
      },
    };
  }

  get activeGroup() {
    return this.session.service?.id;
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

  get documentListColumns() {
    if (macroCondition(getOwnConfig().application === "gr")) {
      return {
        type: {
          label: "type",
          labelHidden: true,
        },
        title: {
          label: "document-title",
          sort: true,
        },
        marks: {
          label: "marks",
          labelHidden: true,
        },
        date: {
          label: "date",
          sort: true,
          sortKey: "created_at",
        },
        modifiedAt: {
          label: "modified-at",
          sort: true,
          sortKey: "modified_at",
        },
        createdByUser: {
          label: "created-by-user",
          sort: true,
          sortKey: "created_by_username",
        },
        createdByGroup: {
          label: "created-by-group",
          sort: true,
          sortKey: "group_name",
        },
        category: {
          label: "category",
          sort: true,
          sortKey: "category__name",
        },
      };
    }

    // Fallback of null means that the default alexandria columns will be used
    return null;
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

    let url;
    let label = instance.dossierNumber;
    let isExternal = false;

    if (this.ebauModules.isLegacyApp) {
      const baseUrl = `/index/redirect-to-instance-resource/instance-id/${instance.id}`;
      const emberUrl = this.router.urlFor("alexandria", {
        queryParams: { document: document.id },
      });

      url = `${baseUrl}?instance-resource-name=alexandria&ember-hash=${emberUrl}`;
      isExternal = true;
    } else {
      url = this.router.urlFor("cases.detail.alexandria", instance, {
        queryParams: {
          document: document.id,
        },
      });
    }

    if (macroCondition(getOwnConfig().application === "be")) {
      label = instance.ebauNumber;
    }

    return { url, label, isExternal };
  }

  namespace = "/alexandria/api/v1";
  zipDownloadNamespace = "/alexandria";
  enablePDFConversion = true;
  enableWebDAV = true;
  allowedWebDAVMimeTypes = allowedWebDAVMimeTypes();
  enableOriginalDocumentFilename = enableOriginalDocumentFilename;
}
