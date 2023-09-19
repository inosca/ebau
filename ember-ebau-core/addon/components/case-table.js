import { action } from "@ember/object";
import { inject as service } from "@ember/service";
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
      intent: {
        searchAnswers: [
          {
            questions: mainConfig.intentSlugs,
            lookup: "CONTAINS",
            value: filter.intent,
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
      parcel: {
        searchAnswers: [
          {
            questions: caseTableConfig.parcelSlugs,
            lookup: "CONTAINS",
            value: filter.parcel,
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
          }
        : macroCondition(getOwnConfig().application === "gr")
          ? {
              personalDetails: {
                searchAnswers: [
                  {
                    questions: [
                      "name-juristische-person-gesuchstellerin",
                      "name-gesuchstellerin",
                      "vorname-gesuchstellerin",
                    ],
                    value: filter.personalDetails,
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
              form: {
                documentForms: filter.form?.split(","),
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
                address: undefined,
                parcel: undefined,
                ...(this.args.casesBackend === "camac-ng"
                  ? { intent: undefined }
                  : {}),
              }
            : macroCondition(getOwnConfig().application === "be")
              ? {
                  dossierNumber: {
                    metaValue: [
                      {
                        key: "ebau-number",
                        value: filter.dossierNumber,
                      },
                    ],
                  },
                  form: {
                    documentForms: filter.form?.split(","),
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
        ([key, value]) => Boolean(value) && Boolean(availableFilterSet[key]),
      )
      .map(([key]) => availableFilterSet[key]);

    const workflow = this.args.workflow;
    const excludeWorkflow = this.args.excludeWorkflow;
    return [
      { excludeChildCases: true },
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
      responsible_service: this.args.filter.responsibleMunicipality,
      ...(macroCondition(getOwnConfig().application === "sz")
        ? {
            address_sz: this.args.filter.address,
            plot_sz: this.args.filter.parcel,
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
            ...(this.args.casesBackend === "camac-ng"
              ? { intent_sz: this.args.filter.intent }
              : {}),
            keyword_search: this.args.filter.keywordSearch,
            location: this.args.filter.municipality,
            caluma_keyword_search: this.args.filter.calumaKeywordSearch,
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
              is_paper: this.args.filter.paper,
              oereb_legal_state: this.args.filter.legalStateOereb,
              location: this.args.filter.municipality,
            }
          : macroCondition(getOwnConfig().application === "be")
            ? {
                tags: this.args.filter.keywords,
                is_paper: this.args.filter.paper,
                is_modification: this.args.filter.modification,
                inquiry_state: this.args.filter.inquiryState,
                decision_date_before: this.args.filter.decisionDateBefore,
                decision_date_after: this.args.filter.decisionDateAfter,
                decision: this.args.filter.decision,
                inquiry_created_before: this.args.filter.inquiryCreatedBefore,
                inquiry_created_after: this.args.filter.inquiryCreatedAfter,
                inquiry_completed_before:
                  this.args.filter.inquiryCompletedBefore,
                inquiry_completed_after: this.args.filter.inquiryCompletedAfter,
                inquiry_answer: this.args.filter.inquiryAnswer,
              }
            : macroCondition(getOwnConfig().application === "gr")
              ? {
                  keywords: this.args.filter.keywords,
                  decision: this.args.filter.decision,
                  is_paper: this.args.filter.paper,
                }
              : macroCondition(getOwnConfig().application === "so")
                ? {
                    keywords: this.args.filter.keywords,
                    is_paper: this.args.filter.paper,
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
      : tableColumns[this.ebauModules.baseRole] ?? tableColumns.default ?? [];

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

    let redirectToPortal =
      caseRecord.instance.isPaper &&
      parseInt(caseRecord.instance.get("instanceState.id")) ===
        parseInt(mainConfig.instanceStates?.new);

    if (hasFeature("permissions.municipalityBeforeSubmission")) {
      const permissions = await this.store.query("instance-permission", {
        instance_id: instanceId,
      });

      redirectToPortal =
        redirectToPortal ||
        (permissions[0]?.permissions.includes("redirect-to-portal") ?? false);
    }

    let url = `/index/redirect-to-instance-resource/instance-id/${instanceId}/`;

    if (redirectToPortal) {
      const portalURL = getOwnConfig().portalUrl;
      const group = this.ebauModules.groupId;
      const language = this.ebauModules.language;
      url = `${portalURL}/instances/${instanceId}?group=${group}&language=${language}&referrer=internal`;
    } else if (this.ebauModules.applicationName === "ebau") {
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
