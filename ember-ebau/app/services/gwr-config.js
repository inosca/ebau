import { action } from "@ember/object";
import Service, { inject as service } from "@ember/service";
import mainConfig from "ember-ebau-core/config/main";

import ENV from "ebau/config/environment";

export default class GwrConfigService extends Service {
  @service session;
  @service store;

  gwrAPI = "/housing-stat/regbl/api/ech0216/2";
  isTestEnvironment = ENV.appEnv !== "production";
  pageSize = 10;
  projectSortColumn = "bau_modify_date";
  projectSortDirection = "desc";
  buildingSortColumn = "geb_modify_date";
  buildingSortDirection = "desc";
  quarterlyClosureSortColumn = "bau_create_date";
  quarterlyClosureSortDirection = "desc";

  get modalContainer() {
    return mainConfig.gwr.modalContainer;
  }

  get importModels() {
    return mainConfig.gwr.importModels;
  }

  get cantonAbbreviation() {
    return mainConfig.gwr.cantonAbbreviation;
  }

  get authToken() {
    return this.session.data.authenticated.access_token;
  }

  get camacGroup() {
    return this.session.group;
  }

  @action
  async fetchInstanceLinks(localIds) {
    const instances = await this.store.query("instance", {
      instance_id: [...new Set(localIds)].join(","),
    });
    return instances.map(({ id, dossierNumber }) => ({
      localId: id,
      identifier: dossierNumber,
      hostLink: `/cases/${id}/gwr`,
    }));
  }
}
