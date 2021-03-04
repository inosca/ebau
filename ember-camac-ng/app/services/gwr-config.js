import Service from "@ember/service";

export default class GwrConfigService extends Service {
  municipalityId = 1342;
  municipalityName = "Galgenen";
  cantonAbbreviation = "SZ";
  constructionSurveyDept = 134200;
  gwrAPI = "/housing-stat/regbl/api/ech0216/2";
}
