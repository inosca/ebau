import Service, { inject as service } from "@ember/service";

import ENV from "camac-ng/config/environment";

export default class GwrConfigService extends Service {
  @service session;
  @service shoebox;

  gwrAPI = "/housing-stat/regbl/api/ech0216/2";

  get cantonAbbreviation() {
    return ENV.APPLICATION.GWRCantonAbbreviation;
  }

  get authToken() {
    return this.session.data.authenticated.access_token;
  }

  get camacGroup() {
    return this.shoebox.content.groupId;
  }
}
