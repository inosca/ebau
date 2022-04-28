import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";
import { objectFromQueryParams } from "ember-ebau-core/decorators";

import filterConfig from "camac-ng/ui/components/case-filter/filter-config";

export default class CasesIndexController extends Controller {
  queryParams = [
    "displaySearch",
    "hasActivation",
    "hasPendingBillingEntry",
    "hasPendingSanction",
    "workflow",
    "excludeWorkflow",
    "isCaluma",
    "instanceStates",
    ...Object.keys(filterConfig),
  ];

  @tracked displaySearch = false;
  @tracked hasActivation = null;
  @tracked hasPendingBillingEntry = null;
  @tracked hasPendingSanction = null;
  @tracked workflow = null;
  @tracked excludeWorkflow = null;
  @tracked isCaluma = null;
  @tracked instanceStates = null;

  @objectFromQueryParams(filterConfig)
  caseFilter;

  get casesBackend() {
    return (this.isCaluma ?? "true") === "true" ? "caluma" : "camac-ng";
  }

  @action
  setCaseFilter(filter) {
    this.caseFilter = filter;
  }
}
