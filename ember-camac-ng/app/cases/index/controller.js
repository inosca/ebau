import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import filterConfig from "ember-ebau-core/components/case-filter/filter-config";
import caseTableConfig from "ember-ebau-core/config/case-table";
import { objectFromQueryParams } from "ember-ebau-core/decorators";

import { moduleConfig } from "camac-ng/decorators";

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

  @tracked isReady = false;

  constructor(...args) {
    super(...args);

    if (!this.displaySearch) {
      this.isReady = true;
    }
  }

  get casesBackend() {
    return this.isCaluma ?? true ? "caluma" : "camac-ng";
  }

  @action
  setCaseFilter(filter) {
    // This will be called from the constructor of the case-filter component to
    // apply filters stored in the localstorage. To avoid multiple queries, we
    // only render the table once readiness was declared.
    if (!this.isReady) {
      this.isReady = true;
    }

    this.caseFilter = filter;
  }
}
