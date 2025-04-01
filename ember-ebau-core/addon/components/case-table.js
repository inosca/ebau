import { action } from "@ember/object";
import { service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import { getOwnConfig, macroCondition } from "@embroider/macros";
import Component from "@glimmer/component";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";
import { DateTime } from "luxon";

import caseTableConfig from "ember-ebau-core/config/case-table";
import mainConfig from "ember-ebau-core/config/main";
import caseInstanceIdsQuery from "ember-ebau-core/gql/queries/case-instance-ids.graphql";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class CaseTableComponent extends Component {
  @service store;
  @service intl;
  @service fetch;
  @service notification;
  @service router;
  @service ebauModules;
  @service permissions;

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

  get showEntries() {
    if (!this.ebauModules.isSupportRole) {
      return true;
    }

    return Object.values(this.args.filter).some((filter) => !isEmpty(filter));
  }

  get isService() {
    return this.ebauModules.baseRole === "service";
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
            key: mainConfig.answerSlugs.specialId,
            lookup: caseTableConfig.specialIdLookup || "ICONTAINS",
            value: filter.dossierNumber,
          },
        ],
      },
      caseCreatedDateBefore: {
        createdBefore: DateTime.fromISO(filter.caseCreatedDateBefore)
          .endOf("day")
          .toISO(),
      },

      caseCreatedDateAfter: {
        createdAfter: DateTime.fromISO(filter.caseCreatedDateAfter)
          .startOf("day")
          .toISO(),
      },
      parcel: {
        searchAnswers: [
          {
            questions: caseTableConfig.parcelSlugs || [
              mainConfig.answerSlugs.parcelNumber,
            ],
            // TODO communicate change of behavior for BE, GR, AG
            lookup: "EXACT_WORD",
            value: filter.parcel,
          },
        ],
      },
      form: {
        documentForms: filter.form?.split(","),
      },
      personalDetails: {
        searchAnswers: [
          {
            questions: caseTableConfig.personalDetailsSlugs,
            value: filter.personalDetails,
          },
        ],
      },
      appeal: {
        metaValue: [
          {
            key: "is-appeal",
            lookup: "EXACT",
            value: true,
          },
        ],
        invert: filter.appeal !== "1",
      },
      ...(this.args.casesBackend !== "camac-ng"
        ? {
            intent: {
              searchAnswers: [
                {
                  questions: mainConfig.intentSlugs,
                  lookup: "CONTAINS",
                  value: filter.intent,
                },
              ],
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
            address: {
              searchAnswers: [
                {
                  questions: caseTableConfig.addressSlugs,
                  lookup: "CONTAINS",
                  value: filter.address,
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
          }
        : {}),
      // BE-specific
      freetext: {
        searchAnswers: [
          {
            questions: mainConfig.freetextSlugs,
            lookup: "CONTAINS",
            value: filter.freetext,
          },
        ],
      },
      // UR-specific
      buildingPermitType: {
        hasAnswer: [
          {
            question: "form-type",
            lookup: "IN",
            value: filter.buildingPermitType,
          },
        ],
      },
      // SZ-specific
      caseStatus: {
        status: filter.caseStatus,
      },
      caseDocumentFormName: {
        documentForm: filter.form,
      },
    };

    const searchFilters = Object.entries(filter)
      .filter(
        ([key, value]) => Boolean(value) && Boolean(availableFilterSet[key]),
      )
      .map(([key]) => availableFilterSet[key]);

    const workflow = this.args.workflow;
    const excludeWorkflow = this.args.excludeWorkflow;
    return [
      { excludeChildCases: true },
      { metaHasKey: "camac-instance-id" },
      ...searchFilters,
      ...(workflow ? [{ workflow }] : []),
      ...(excludeWorkflow ? [{ workflow: excludeWorkflow, invert: true }] : []),
    ];
  }

  get keywordFilterName() {
    return caseTableConfig.useLegacyTags ? "tags" : "keywords";
  }

  get camacFilter() {
    const filters = {
      instance_state:
        this.args.filter.instanceState || this.args.instanceStates || "",
      service: this.args.filter.service || this.args.filter.serviceSZ,
      responsible_service_user: this.args.filter.responsibleServiceUser,
      responsible_service: this.args.filter.responsibleMunicipality,
      is_paper: this.args.filter.paper,
      [this.keywordFilterName]: this.args.filter.keywords,
      decision: this.args.filter.decision,
      inquiry_created_before: this.args.filter.inquiryCreatedBefore,
      inquiry_created_after: this.args.filter.inquiryCreatedAfter,
      inquiry_completed_before: this.args.filter.inquiryCompletedBefore,
      inquiry_completed_after: this.args.filter.inquiryCompletedAfter,
      inquiry_state: this.args.filter.inquiryState,
      inquiry_answer: this.args.filter.inquiryAnswer,
      // BE-specific
      is_modification: this.args.filter.modification,
      decision_date_before: this.args.filter.decisionDateBefore,
      decision_date_after: this.args.filter.decisionDateAfter,
      // UR-specific
      circulation_state: this.args.hasActivation
        ? caseTableConfig.activeCirculationStates
        : null,
      has_pending_billing_entry: this.args.hasPendingBillingEntry,
      has_pending_sanction: this.args.hasPendingSanction,
      pending_sanctions_control_instance:
        this.args.filter.pendingSanctionsControlInstance,
      with_cantonal_participation: this.args.filter.withCantonalParticipation,
      oereb_legal_state: this.args.filter.legalStateOereb,
      // SZ-specific
      caluma_keyword_search: this.args.filter.calumaKeywordSearch,
      ...(this.args.casesBackend === "camac-ng"
        ? {
            location: this.args.filter.municipality,
            intent_sz: this.args.filter.intent,
            address_sz: this.args.filter.address,
            plot_egrid_sz: this.args.filter.parcel_egrid,
            plot_number_sz: this.args.filter.parcel_property_number,
            builder_sz: this.args.filter.builder,
            landowner_sz: this.args.filter.landowner,
            applicant_sz: this.args.filter.applicant,
            submit_date_after_sz: this.args.filter.submitDateAfter,
            submit_date_before_sz: this.args.filter.submitDateBefore,
            form_name_versioned: this.args.filter.type,
            objection_received: this.args.filter.objectionReceived,
            construction_zone_location_sz:
              this.args.filter.constructionZoneLocation,
            identifier: this.args.filter.instanceIdentifier || "",
            keyword_search: this.args.filter.keywordSearch,
          }
        : {}),
    };

    return {
      "x-camac-filters": Object.entries(filters)
        .filter(([, value]) => ![null, undefined, ""].includes(value))
        .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
        .join("&"),
    };
  }

  async processNew(cases) {
    if (!cases.length) {
      return [];
    }

    const instanceIds = cases.map((_case) => _case.meta["camac-instance-id"]);

    if (macroCondition(getOwnConfig().application === "ur")) {
      if (this.isService) {
        await this.store.query("activation", {
          instance: instanceIds.join(","),
          service: this.ebauModules.serviceId,
          include: "circulation",
        });

        await this.store.query("responsible-service", {
          include: "responsible_user",
          instance: instanceIds.join(","),
        });
      }
    }

    await this.store.query("instance", {
      instance_id: instanceIds.join(","),
      include: [
        "instance_state",
        ...(macroCondition(getOwnConfig().application === "ur")
          ? ["circulation_initializer_services", "user"]
          : []),
        ...(macroCondition(getOwnConfig().application === "sz")
          ? ["form", "user"]
          : []),
      ].join(","),
      ...(macroCondition(getOwnConfig().application === "be")
        ? {
            "fields[instances]":
              "id,name,decision,decision_date,involved_at,instance_state,is_paper,ebau_number",
          }
        : {}),
      ...(macroCondition(getOwnConfig().application === "gr")
        ? {
            "fields[instances]": "id,name,decision,instance_state,involved_at",
          }
        : {}),
      ...(macroCondition(getOwnConfig().application === "so")
        ? {
            "fields[instances]": "id,name,decision,instance_state,is_paper",
          }
        : {}),
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
      : (tableColumns[this.ebauModules.baseRole] ?? tableColumns.default ?? []);

    const availableOrderings = Object.keys(
      caseTableConfig.availableOrderings ?? [],
    );

    return columnNames.map((name) => ({
      name,
      order: availableOrderings.find((ordering) => ordering === name),
    }));
  }

  @action
  async redirectToCase(caseRecord) {
    const instanceId = caseRecord.instanceId;

    const isNewCase =
      parseInt(caseRecord.instance.get("instanceState.id")) ===
      parseInt(mainConfig.instanceStates?.new);

    let redirectToPortal = caseRecord.instance.isPaper && isNewCase;
    if (hasFeature("permissions.municipalityBeforeSubmission")) {
      redirectToPortal ||= await this.permissions.hasAny(
        instanceId,
        "redirect-to-portal",
      );
    }

    if (hasFeature("internalCaseCreation")) {
      redirectToPortal = false;
    }

    let url = `/index/redirect-to-instance-resource/instance-id/${instanceId}/`;

    if (redirectToPortal) {
      const portalURL = getOwnConfig().portalUrl;
      const group = this.ebauModules.groupId;
      const language = this.ebauModules.language;
      url = `${portalURL}/instances/${instanceId}?group=${group}&language=${language}&referrer=internal`;
    } else if (!this.ebauModules.isLegacyApp) {
      return this.router.transitionTo("cases.detail", instanceId);
    }

    location.assign(url);
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
          fetchPolicy: "network-only",
          variables: { filter: this.gqlFilter },
          context: {
            headers: this.camacFilter,
          },
        },
        "allCases.edges",
      );

      const ids = response.map((edge) => edge.node.meta["camac-instance-id"]);

      const exportResponse = yield this.fetch.fetch(
        `/api/v1/instances/export?instance_id=${ids.join(",")}`,
      );

      saveAs(yield exportResponse.blob(), "export.xlsx");
    } catch {
      this.notification.danger(this.intl.t("cases.export.error"));
    }
  }
}
