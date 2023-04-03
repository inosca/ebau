import { inject as service } from "@ember/service";
import { dasherize } from "@ember/string";
import RESTAdapter from "@ember-data/adapter/rest";
import { singularize } from "ember-inflector";

export default class TemplateAdapter extends RESTAdapter {
  @service session;

  namespace = "document-merge-service/api/v1";

  pathForType(modelName) {
    return singularize(dasherize(modelName));
  }

  buildURL(modelName, id) {
    return `${super.buildURL(modelName, id)}/`;
  }

  ajaxOptions(url, type, options) {
    const ajaxOptions = super.ajaxOptions(url, type, options);

    if (type === "PUT") {
      // Use PATCH instead of PUT for updating records
      ajaxOptions.type = "PATCH";
      ajaxOptions.method = "PATCH";
    }

    if (type === "PUT" || type === "POST") {
      // Remove content type for updating and creating records so the content
      // type will be defined by the passed form data
      delete ajaxOptions.headers["content-type"];
    }

    return ajaxOptions;
  }

  get headers() {
    return this.session.authHeaders;
  }

  async ajax(...args) {
    // Refresh the token (only needed for ember-camac-ng)
    await this.session.getAuthorizationHeader?.();

    return await super.ajax(...args);
  }

  normalizeErrorResponse(status, headers, payload) {
    return [{ status, detail: payload }];
  }

  generatedDetailedMessage(status, headers, payload) {
    return payload.detail;
  }
}
