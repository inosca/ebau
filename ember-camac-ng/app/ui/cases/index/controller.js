import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { objectFromQueryParams } from "ember-ebau-core/decorators";

import caseTableConfig from "camac-ng/config/case-table";
import { moduleConfig } from "camac-ng/decorators";
import filterConfig from "camac-ng/ui/components/case-filter/filter-config";

export default class CasesIndexController extends Controller {
  @service shoebox;

  queryParams = ["order", ...Object.keys(filterConfig)];

  @moduleConfig("cases", "displaySearch", false) displaySearch;
  @moduleConfig("cases", "hasActivation", null) hasActivation;
  @moduleConfig("cases", "hasPendingBillingEntry", null) hasPendingBillingEntry;
  @moduleConfig("cases", "hasPendingSanction", null) hasPendingSanction;
  @moduleConfig("cases", "workflow", null) workflow;
  @moduleConfig("cases", "excludeWorkflow", null) excludeWorkflow;
  @moduleConfig("cases", "isCaluma", null) isCaluma;
  @moduleConfig("cases", "instanceStates", null) instanceStates;

  @objectFromQueryParams(filterConfig)
  caseFilter;

  @tracked order = caseTableConfig.defaultOrder;

  get casesBackend() {
    return this.isCaluma ?? true ? "caluma" : "camac-ng";
  }

  @action
  setCaseFilter(filter) {
    this.caseFilter = filter;
  }
}
