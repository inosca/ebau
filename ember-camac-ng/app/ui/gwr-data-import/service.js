import Service, { inject as service } from "@ember/service";

export default class GwrDataImportService extends Service {
  @service fetch;
  async fetchProject(instanceId) {
    const data = await this.fetch.fetch(
      `/api/v1/instances/${instanceId}/gwr_data`,
      {
        headers: {
          accept: "application/json",
        },
      }
    );
    return await data.json();
  }

  async fetchBuildings() {}

  async fetchDwellings() {}

  async fetchEntrances() {}
}
