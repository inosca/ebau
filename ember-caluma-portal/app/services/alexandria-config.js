import { tracked } from "@glimmer/tracking";
import AlexandriaConfigService from "ember-alexandria/services/alexandria-config";

export default class CustomAlexandriaConfigService extends AlexandriaConfigService {
  @tracked instanceId;
  @tracked documentId;

  namespace = "alexandria/api/v1";

  get defaultModelMeta() {
    return {
      document: {
        "camac-instance-id": String(this.instanceId),
        "caluma-document-id": this.documentId,
      },
    };
  }

  // Must be kept in sync with the `customMimeTypes` of the alexandria config
  // service in `ember-ebau-core`. This service intentionally doesn't extend
  // that one, so the types have to be duplicated here.
  customMimeTypes = {
    "application/vnd.ms-outlook": ["msg"],
    "application/geopackage+sqlite3": ["gpkg"],
    // txt needs to be first in order to be the extension that is returned when
    // calling `mime.getExtension("text/plain")`
    "text/plain": ["txt", "ili"],
  };
}
