import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";
import filterConfig from "ember-ebau-core/components/case-filter/filter-config";
import caseTableConfig from "ember-ebau-core/config/case-table";
import { objectFromQueryParams } from "ember-ebau-core/decorators";

export default class CasesIndexController extends Controller {
  queryParams = [
    "order",
    "displaySearch",
    // "hasActivation",
    "hasPendingBillingEntry",
    // "hasPendingSanction",
    // "workflow",
    // "excludeWorkflow",
    // "isCaluma",
    "instanceStates",
    ...Object.keys(filterConfig),
  ];

  get parsedInstanceStates() {
    return this.instanceStates?.split(",") ?? [];
  }

  // This is the legacy implementation of taking default filters from the PHP
  // shoebox. In a non-embedded ember app this is not possible which is why we
  // currently take only the needed parameters from the URL (exposed in
  // `django/camac/core/serializers.py::ResourceSerializer.get_link`)
  //
  // @moduleConfig("cases", "displaySearch", false) displaySearch;
  // @moduleConfig("cases", "hasActivation", null) hasActivation;
  // @moduleConfig("cases", "hasPendingBillingEntry", null) hasPendingBillingEntry;
  // @moduleConfig("cases", "hasPendingSanction", null) hasPendingSanction;
  // @moduleConfig("cases", "workflow", null) workflow;
  // @moduleConfig("cases", "excludeWorkflow", null) excludeWorkflow;
  // @moduleConfig("cases", "isCaluma", null) isCaluma;
  // @moduleConfig("cases", "instanceStates", null) instanceStates;

  @objectFromQueryParams(filterConfig)
  caseFilter;

  @tracked order = caseTableConfig.defaultOrder;
  @tracked displaySearch = false;
  @tracked hasPendingBillingEntry = null;
  @tracked instanceStates = null;

  @tracked isReady = false;

  constructor(...args) {
    super(...args);

    if (!this.displaySearch) {
      this.isReady = true;
    }
  }

  get casesBackend() {
    return (this.isCaluma ?? true) ? "caluma" : "camac-ng";
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
