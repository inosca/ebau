import Service, { inject as service } from "@ember/service";
import { saveAs } from "file-saver";

export default class DmsService extends Service {
  @service fetch;

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
}
