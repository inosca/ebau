import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import moment from "moment";

import config from "camac-ng/config/environment";

export default class CaseTableComponent extends Component {
  @service store;
  @service intl;
  @service shoebox;

  @calumaQuery({ query: allCases, options: "options" }) casesQuery;

  get options() {
    return {
      pageSize: 15,
      processNew: (cases) => this.processNew(cases),
    };
  }

  get isService() {
    return this.shoebox.role === "service";
  }

  get gqlFilter() {
    const filter = this.args.filter;
    const availableFilterSet = {
      buildingPermitType: {
        hasAnswer: [
          {
            question: "form-type",
            value: filter.buildingPermitType,
          },
        ],
      },
      instanceId: {
        metaValue: [
          {
            key: "camac-instance-id",
            value: filter.instanceId,
          },
        ],
      },
      dossierNumber: {
        metaValue: [
          {
            key: "dossier-number",
            lookup: "CONTAINS",
            value: filter.dossierNumber,
          },
        ],
      },
      createdBefore: {
        metaValue: [
          {
            key: "submit-date",
            lookup: "LTE",
            value: moment.utc(filter.createdBefore).endOf("day"),
          },
        ],
      },
      createdAfter: {
        metaValue: [
          {
            key: "submit-date",
            lookup: "GTE",
            value: moment.utc(filter.createdAfter).startOf("day"),
          },
        ],
      },
      intent: {
        searchAnswers: [
          {
            questions: config.APPLICATION.intentSlugs,
            lookup: "CONTAINS",
            value: filter.intent,
          },
        ],
      },
      applicantName: {
        searchAnswers: [
          {
            questions: ["first-name", "last-name", "juristic-person-name"],
            lookup: "CONTAINS",
            value: filter.applicantName,
          },
        ],
      },
      street: {
        searchAnswers: [
          {
            questions: ["parcel-street", "street-number", "parcel-city"],
            lookup: "CONTAINS",
            value: filter.street,
          },
        ],
      },
      parcelNumber: {
        hasAnswer: [
          {
            question: "parcel-number",
            lookup: "CONTAINS",
            value: filter.parcelNumber,
          },
        ],
      },
      caseStatus: {
        status: filter.caseStatus,
      },
      caseDocumentFormName: {
        documentForm: filter.caseDocumentFormName,
      },
    };

    const searchFilters = Object.entries(filter)
      .filter(
        ([key, value]) => Boolean(value) && Boolean(availableFilterSet[key])
      )
      .map(([key]) => availableFilterSet[key]);

    const workflow = this.args.workflow;
    return [...searchFilters, ...(workflow ? [{ workflow }] : [])];
  }

  get paginationInfo() {
    return htmlSafe(
      this.intl.t("global.paginationInfo", {
        count: this.casesQuery.value.length,
        total: this.casesQuery.totalCount,
      })
    );
  }

  async processNew(cases) {
    if (!cases.length) {
      return [];
    }
    const instanceIds = cases.map((_case) => _case.meta["camac-instance-id"]);

    if (this.isService) {
      await this.store.query("activation", {
        instance: instanceIds.join(","),
        service: this.shoebox.content.serviceId,
        include: "circulation",
      });
    }

    await this.store.query("instance", {
      instance_id: instanceIds.join(","),
      include: "instance_state,user,form",
    });
    return cases;
  }

  get tableColumns() {
    const tableColumns = config.APPLICATION.caseTableColumns;

    if (Array.isArray(tableColumns)) {
      return tableColumns;
    }

    const role = this.shoebox.role;
    // TODO camac_legacy: Remove this in the future
    return tableColumns[role] ?? tableColumns.default ?? [];
  }

  @action
  setup() {
    const camacFilters = {
      instance_state: this.args.filter.instanceState || "",
      location: this.args.filter.municipality,
      service: this.args.filter.service,
      circulation_state: this.args.hasActivation
        ? config.APPLICATION.activeCirculationStates
        : null,
      has_pending_billing_entry: this.args.hasPendingBillingEntry,
      has_pending_sanction: this.args.hasPendingSanction,
      pending_sanctions_control_instance:
        this.args.filter.pendingSanctionsControlInstance,
    };
    this.casesQuery.fetch({
      order: [{ meta: "dossier-number" }],
      filter: this.gqlFilter,
      queryOptions: {
        context: {
          headers: {
            "x-camac-filters": Object.entries(camacFilters)
              .filter(([, value]) => value)
              .map((entry) => entry.join("="))
              .join("&"),
          },
        },
      },
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
