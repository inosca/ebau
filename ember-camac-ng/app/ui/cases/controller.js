import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allCases } from "ember-caluma/caluma-query/queries";

export default class CasesController extends Controller {
  queryParams = ["caseStates"];
  @tracked caseStates;

  @service store;
  @service intl;
  @service shoebox;

  @calumaQuery({ query: allCases, options: "options" }) casesQuery;

  get options() {
    return {
      pageSize: 15,
      processNew: cases => this.processNew(cases),
      queryOptions: {
        context: {
          headers: {
            "x-camac-filters": `instance_state=${this.caseStates}`
          }
        }
      }
    };
  }

  get paginationInfo() {
    return htmlSafe(
      this.intl.t("global.paginationInfo", {
        count: this.casesQuery.value.length,
        total: this.casesQuery.totalCount
      })
    );
  }

  async processNew(cases) {
    const instanceIds = cases.map(_case => _case.meta["camac-instance-id"]);

    await this.store.query("instance", {
      instance_id: instanceIds.join(","),
      include: "instance_state,user"
    });
    return cases;
  }

  get tableHeaders() {
    // TODO camac_legacy: Remove this in the future
    switch (this.shoebox.role) {
      case "municipality":
        return [
          "instanceId",
          "dossierNr",
          "form",
          "municipality",
          "user",
          "applicant",
          "intent",
          "street",
          "instanceState"
        ];

      case "coordination":
        return [
          "instanceId",
          "dossierNr",
          "coordination",
          "coordinationShort",
          "form",
          "municipality",
          "user",
          "applicant",
          "intent",
          "street",
          "instanceState"
        ];
      case "service":
        return [
          "instanceId",
          "dossierNr",
          "coordination",
          "coordinationShort",
          "form",
          "municipality",
          "applicant",
          "intent",
          "street",
          "reason",
          "caseStatus"
        ];

      default:
        return [
          "dossierNr",
          "municipality",
          "applicant",
          "intent",
          "street",
          "parcel"
        ];
    }
  }

  @action
  setup() {
    this.casesQuery.fetch({ order: [{ meta: "camac-instance-id" }] });
  }

  @action
  loadNextPage() {
    this.casesQuery.fetchMore();
  }

  @action
  redirectToCase(caseRecord) {
    location.assign(
      `/index/redirect-to-instance-resource/instance-id/${caseRecord.instanceId}/`
    );
  }
}
