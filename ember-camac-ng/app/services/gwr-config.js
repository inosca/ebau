import Service, { inject as service } from "@ember/service";

export default class GwrConfigService extends Service {
  @service session;
  @service shoebox;

  municipalityId = 1342;
  cantonAbbreviation = "SZ";
  gwrAPI = "/housing-stat/regbl/api/ech0216/2";

  username = "1342zoselc";
  password = "%u1N89DqX4";

  get constructionSurveyDeptNumber() {
    return `${this.municipalityId}00`;
  }

  get authToken() {
    return this.session.data.authenticated.access_token;
  }

  get camacGroup() {
    return this.shoebox.content.groupId;
  }
}
