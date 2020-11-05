import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";

import { objectFromQueryParams } from "camac-ng/decorators";

const filterQueryParams = [
  "dossierNumber",
  "municipality",
  "parcelNumber",
  "instanceState",
  "buildingPermitType",
  "createdAfter",
  "createdBefore",
  "proposalDescription",
  "applicantName",
];

export default class CasesIndexController extends Controller {
  queryParams = ["displaySearch", ...filterQueryParams];

  @tracked displaySearch = false;

  @objectFromQueryParams(...filterQueryParams)
  caseFilter;

  @action
  setCaseFilter(filter) {
    this.caseFilter = filter;
  }
}
