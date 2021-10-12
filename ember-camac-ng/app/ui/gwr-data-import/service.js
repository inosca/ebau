import Service, { inject as service } from "@ember/service";

export default class GwrDataImportService extends Service {
  @service fetch;

  async fetchImportData(instanceId) {
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

  async fetchProject(instanceId) {
    return await this.fetchImportData(instanceId);
  }

  async fetchBuildings(instanceId) {
    const importData = await this.fetchImportData(instanceId);
    return importData.work;
  }

  async fetchDwellings(instanceId) {
    const importData = await this.fetchImportData(instanceId);
    return importData.work.flatMap(
      (buildingWork) => buildingWork.building.dwellings
    );
  }

  async fetchEntrances() {}
}
