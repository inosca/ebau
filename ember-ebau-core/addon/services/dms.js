import Service, { service } from "@ember/service";
import { findRecord } from "ember-data-resources";
import { saveAs } from "file-saver";

export default class DmsService extends Service {
  @service fetch;
  @service ebauModules;

  async generatePdf(instanceId, params = {}) {
    const query = Object.entries(params)
      .map(([k, v]) => `${k}=${v}`)
      .join("&");

    const fullQuery = query ? `?${query}` : "";
    const response = await this.fetch.fetch(
      `/api/v1/instances/${instanceId}/generate-pdf${fullQuery}`,
    );

    const filename = response.headers
      .get("content-disposition")
      .match(/filename="(.*)"/)[1];

    saveAs(await response.blob(), filename);
  }

  service = findRecord(this, "service", () => [
    this.ebauModules.serviceId,
    { include: "service_group" },
  ]);

  get serviceSlug() {
    return this.service.record?.slug;
  }

  get serviceGroupSlug() {
    return this.service.record?.serviceGroup.get("slug");
  }

  get serviceGroupName() {
    return this.service.record?.serviceGroup.get("name");
  }
}
