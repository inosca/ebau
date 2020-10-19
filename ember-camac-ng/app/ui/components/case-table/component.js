import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import calumaQuery from "ember-caluma/caluma-query";
import { allCases } from "ember-caluma/caluma-query/queries";

export default class CaseTableComponent extends Component {
  @service store;
  @service intl;
  @service shoebox;

  @calumaQuery({ query: allCases, options: "options" }) casesQuery;

  get options() {
    return {
      pageSize: 15,
      processNew: cases => this.processNew(cases)
    };
  }

  get gqlFilter() {
    const filter = this.args.filter;
    const availableFilterSet = {
      buildingPermitType: {
        hasAnswer: [
          {
            question: "building-permit-type",
            value: filter.buildingPermitType
          }
        ]
      },
      dossierNumber: {
        metaValue: [
          {
            key: "dossier-number",
            value: filter.dossierNumber
          }
        ]
      },
      proposalDescription: {
        hasAnswer: [
          {
            question: "proposal-description",
            lookup: "ICONTAINS",
            value: filter.proposalDescription
          }
        ]
      },
      createdBefore: { createdBefore: filter.createdBefore },
      createdAfter: { createdAfter: filter.createdAfter }
    };

    return Object.entries(filter)
      .filter(
        ([key, value]) => Boolean(value) && Boolean(availableFilterSet[key])
      )
      .map(([key]) => availableFilterSet[key]);
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
      include: "instance_state,user,form"
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
    this.casesQuery.fetch({
      order: [{ meta: "camac-instance-id" }],
      filter: this.gqlFilter,
      queryOptions: {
        context: {
          headers: {
            "x-camac-filters": `instance_state=${this.args.filter
              .instanceState ?? ""}&location=${this.args.filter.municipality}`
          }
        }
      }
    });
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
