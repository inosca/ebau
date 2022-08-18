import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import { getOwnConfig, macroCondition } from "@embroider/macros";
import Component from "@glimmer/component";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";
import { DateTime } from "luxon";

import caseModelConfig from "camac-ng/config/case-model";
import caseTableConfig from "camac-ng/config/case-table";
import caseInstanceIdsQuery from "camac-ng/gql/queries/case-instance-ids.graphql";

export default class CaseTableComponent extends Component {
  @service store;
  @service intl;
  @service shoebox;
  @service fetch;
  @service notification;

  @queryManager apollo;

  casesQuery = useCalumaQuery(this, allCases, () => ({
    options: {
      pageSize: caseTableConfig.pageSize || 15,
      processNew: (cases) => this.processNew(cases),
    },
    ...this.gqlOrder,
    filter: this.gqlFilter,
    queryOptions: {
      context: {
        headers: {
          ...this.camacFilter,
          ...this.camacOrder,
        },
      },
    },
  }));

  get isService() {
    return this.shoebox.baseRole === "service";
  }

  get order() {
    const config =
      caseTableConfig.availableOrderings[this.args.order.replace(/^-/, "")];
    const direction = this.args.order.startsWith("-") ? "ASC" : "DESC";

    if (
      Object.keys(config).includes("caluma") &&
      Object.keys(config).includes("camac-ng")
    ) {
      return {
        [this.args.casesBackend]: config[this.args.casesBackend],
        direction,
      };
    }

    return { ...config, direction };
  }

  get gqlOrder() {
    const config = this.order.caluma;

    return config
      ? {
          order: config.map((orderConfig) => ({
            ...orderConfig,
            direction: orderConfig.direction ?? this.order.direction,
          })),
        }
      : {};
  }

  get camacOrder() {
    const config = this.order["camac-ng"];
    const inverted = this.order.direction === "DESC";

    return config
      ? {
          "x-camac-order": config
            .map((order) => `${inverted ? "-" : ""}${order}`)
            .join(","),
        }
      : {};
  }

  get gqlFilter() {
    const filter = this.args.filter;
    const availableFilterSet = {
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
            lookup: "ICONTAINS",
            value: filter.dossierNumber,
          },
        ],
      },
      submitDateBefore: {
        metaValue: [
          {
            key: "submit-date",
            lookup: "LTE",
            value: DateTime.fromISO(filter.submitDateBefore)
              .endOf("day")
              .toISO(),
          },
        ],
      },
      submitDateAfter: {
        metaValue: [
          {
            key: "submit-date",
            lookup: "GTE",
            value: DateTime.fromISO(filter.submitDateAfter)
              .startOf("day")
              .toISO(),
          },
        ],
      },
      intent: {
        searchAnswers: [
          {
            questions: caseModelConfig.intentSlugs,
            lookup: "CONTAINS",
            value: filter.intent,
          },
        ],
      },
      ...(macroCondition(getOwnConfig().application === "ur")
        ? {
            buildingPermitType: {
              hasAnswer: [
                {
                  question: "form-type",
                  lookup: "IN",
                  value: filter.buildingPermitType,
                },
              ],
            },
            applicant: {
              searchAnswers: [
                {
                  questions: [
                    "first-name",
                    "last-name",
                    "juristic-person-name",
                  ],
                  lookup: "CONTAINS",
                  value: filter.applicant,
                },
              ],
            },
            address: {
              searchAnswers: [
                {
                  questions: ["parcel-street", "street-number", "parcel-city"],
                  lookup: "CONTAINS",
                  value: filter.address,
                },
              ],
            },
            parcel: {
              searchAnswers: [
                {
                  questions: ["parcel-number", "building-law-number"],
                  lookup: "CONTAINS",
                  value: filter.parcel,
                },
              ],
            },
          }
        : macroCondition(getOwnConfig().application === "sz")
        ? {
            caseStatus: {
              status: filter.caseStatus,
            },
            caseDocumentFormName: {
              documentForm: filter.form,
            },
            submitDateBefore: undefined,
            submitDateAfter: undefined,
          }
        : macroCondition(getOwnConfig().application === "be")
        ? {
            ebauNumber: {
              metaValue: [
                {
                  key: "ebau-number",
                  value: filter.ebauNumber,
                },
              ],
            },
            address: {
              searchAnswers: [
                {
                  questions: [
                    "strasse-flurname",
                    "nr",
                    "ort-grundstueck",
                    "standort-migriert",
                  ],
                  lookup: "CONTAINS",
                  value: filter.address,
                },
              ],
            },
            parcel: {
              searchAnswers: [
                {
                  questions: ["parzellennummer"],
                  lookup: "CONTAINS",
                  value: filter.parcel,
                },
              ],
            },
            form: {
              documentForms: filter.form,
            },
            municipality: {
              hasAnswer: [
                {
                  question: "gemeinde",
                  value: filter.municipality,
                  lookup: "EXACT",
                },
              ],
            },
            personalDetails: {
              searchAnswers: [
                {
                  questions: [
                    // Personalien - Gesuchsteller/in
                    "name-gesuchstellerin",
                    "vorname-gesuchstellerin",
                    "name-juristische-person-gesuchstellerin",
                    // Personalien - Vertreter/in mit Vollmacht
                    "name-juristische-person-vertreterin",
                    "name-vertreterin",
                    "vorname-vertreterin",
                    // Personalien - Gebäudeeigentümer/in
                    "name-juristische-person-grundeigentuemerin",
                    "name-grundeigentuemerin",
                    "vorname-grundeigentuemerin",
                    // Personalien - Projektverfasser/in
                    "name-juristische-person-projektverfasserin",
                    "name-projektverfasserin",
                    "vorname-projektverfasserin",
                  ],
                  value: filter.personalDetails,
                },
              ],
            },
          }
        : {}),
    };

    const searchFilters = Object.entries(filter)
      .filter(
        ([key, value]) => Boolean(value) && Boolean(availableFilterSet[key])
      )
      .map(([key]) => availableFilterSet[key]);

    const workflow = this.args.workflow;
    const excludeWorkflow = this.args.excludeWorkflow;
    return [
      ...searchFilters,
      ...(workflow ? [{ workflow }] : []),
      ...(excludeWorkflow ? [{ workflow: excludeWorkflow, invert: true }] : []),
    ];
  }

  get camacFilter() {
    const filters = {
      instance_state:
        this.args.filter.instanceState || this.args.instanceStates || "",
      service: this.args.filter.service || this.args.filter.serviceSZ,
      responsible_service_user: this.args.filter.responsibleServiceUser,
      responsible_service: this.args.responsibleMunicipality,
      exclude_child_cases: true,
      location: this.args.filter.municipality,
      ...(macroCondition(getOwnConfig().application === "sz")
        ? {
            address_sz: this.args.filter.address,
            intent_sz: this.args.filter.intent,
            plot_sz: this.args.filter.parcel,
            builder_sz: this.args.filter.builder,
            landowner_sz: this.args.filter.landowner,
            applicant_sz: this.args.filter.applicant,
            submit_date_after_sz: this.args.filter.submitDateAfter,
            submit_date_before_sz: this.args.filter.submitDateBefore,
            form_name_versioned: this.args.filter.type,
            identifier: this.args.filter.instanceIdentifier || "",
          }
        : macroCondition(getOwnConfig().application === "ur")
        ? {
            circulation_state: this.args.hasActivation
              ? caseTableConfig.activeCirculationStates
              : null,
            has_pending_billing_entry: this.args.hasPendingBillingEntry,
            has_pending_sanction: this.args.hasPendingSanction,
            pending_sanctions_control_instance:
              this.args.filter.pendingSanctionsControlInstance,
            with_cantonal_participation:
              this.args.filter.withCantonalParticipation,
          }
        : macroCondition(getOwnConfig().application === "be")
        ? {
            location: undefined,
            tags: this.args.filter.tags,
            is_paper: this.args.filter.paper,
            inquiry_state: this.args.filter.inquiryState,
            decision_date_before: this.args.filter.decisionDateBefore,
            decision_date_after: this.args.filter.decisionDateAfter,
            decision: this.args.filter.decision,
          }
        : {}),
    };

    return {
      "x-camac-filters": Object.entries(filters)
        .filter(([, value]) => ![null, undefined, ""].includes(value))
        .map((entry) => entry.join("="))
        .join("&"),
    };
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

      await this.store.query("responsible-service", {
        include: "responsible_user",
        instance: instanceIds.join(","),
      });
    }

    await this.store.query("instance", {
      instance_id: instanceIds.join(","),
      include: "instance_state,user,form,circulation_initializer_services",
    });

    if (this.args.casesBackend === "camac-ng") {
      await this.store.query("form-field", {
        instance: instanceIds.join(","),
        name: (caseTableConfig.formFields ?? []).join(","),
        include: "instance",
      });
    }

    return cases;
  }

  get tableColumns() {
    const tableColumns = caseTableConfig.columns[this.args.casesBackend];

    const columnNames = Array.isArray(tableColumns)
      ? tableColumns
      : tableColumns[this.shoebox.baseRole] ?? tableColumns.default ?? [];

    const availableOrderings = Object.keys(
      caseTableConfig.availableOrderings ?? []
    );

    return columnNames.map((name) => ({
      name,
      order: availableOrderings.find((ordering) => ordering === name),
    }));
  }

  @action
  redirectToCase(caseRecord) {
    location.assign(
      `/index/redirect-to-instance-resource/instance-id/${caseRecord.instanceId}/`
    );
  }

  @dropTask
  *export(event) {
    event.preventDefault();

    try {
      if (this.casesQuery.totalCount > 1000) {
        this.notification.danger(this.intl.t("cases.export.too-many"));
        return;
      }

      const response = yield this.apollo.query(
        {
          query: caseInstanceIdsQuery,
          variables: { filter: this.gqlFilter },
          context: {
            headers: this.camacFilter,
          },
        },
        "allCases.edges"
      );

      const ids = response.map((edge) => edge.node.meta["camac-instance-id"]);

      const exportResponse = yield this.fetch.fetch(
        `/api/v1/instances/export?instance_id=${ids.join(",")}`
      );

      saveAs(yield exportResponse.blob(), "export.xlsx");
    } catch {
      this.notification.danger(this.intl.t("cases.export.error"));
    }
  }
}
