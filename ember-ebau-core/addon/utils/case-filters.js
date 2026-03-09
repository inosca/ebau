import { getOwnConfig, macroCondition } from "@embroider/macros";
import { DateTime } from "luxon";

import caseTableConfig from "ember-ebau-core/config/case-table";
import mainConfig from "ember-ebau-core/config/main";

export function getCalumaFilters(filter, casesBackend) {
  const commonFilters = {
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
          lookup: caseTableConfig.specialIdLookup ?? "ICONTAINS",
          value: filter.dossierNumber,
        },
      ],
    },
    caseCreatedDateBefore: {
      createdBefore: DateTime.fromISO(filter.caseCreatedDateBefore)
        .endOf("day")
        .toUTC()
        .toISO(),
    },

    caseCreatedDateAfter: {
      createdAfter: DateTime.fromISO(filter.caseCreatedDateAfter)
        .startOf("day")
        .toUTC()
        .toISO(),
    },
    form: {
      documentForms: filter.form?.split(","),
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
  };
  const specificFilters = {
    caluma: {
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
            questions: ["first-name", "last-name", "juristic-person-name"],
            lookup: "CONTAINS",
            value: filter.applicant,
          },
        ],
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
      ...(macroCondition(getOwnConfig().application !== "ur")
        ? {
            municipality: {
              hasAnswer: [
                {
                  question: "gemeinde",
                  value: filter.municipality,
                  lookup: "EXACT",
                },
              ],
            },
          }
        : {}),
      parcel: {
        searchAnswers: [
          {
            questions: caseTableConfig.parcelSlugs ?? [
              mainConfig.answerSlugs.parcelNumber,
            ],
            // TODO communicate change of behavior for BE, GR, AG
            lookup: "EXACT_WORD",
            value: filter.parcel,
          },
        ],
      },
      personalDetails: {
        searchAnswers: [
          {
            questions: caseTableConfig.personalDetailsSlugs,
            value: filter.personalDetails,
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
              .toUTC()
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
              .toUTC()
              .toISO(),
          },
        ],
      },
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
      // SZ-specific (interne Dossiers)
      caseStatus: {
        status: filter.caseStatus,
      },
      caseDocumentFormName: {
        documentForm: filter.form,
      },
    },
    "camac-ng": {},
  };
  return {
    ...commonFilters,
    ...specificFilters[casesBackend],
  };
}

export function getCamacFilters({
  filter,
  instanceStates,
  hasActivation,
  hasPendingBillingEntry,
  hasPendingSanction,
  casesBackend,
}) {
  const keywordFilterName = caseTableConfig.useLegacyTags ? "tags" : "keywords";

  const commonFilters = {
    instance_state: filter.instanceState || instanceStates || "",
    service: filter.service || filter.serviceSZ,
    responsible_service_user: filter.responsibleServiceUser,
    responsible_service: filter.responsibleMunicipality,
    is_paper: filter.paper,
    [keywordFilterName]: filter.keywords,
    ["static_keywords"]: filter.staticKeywords,
    decision: filter.decision,
    inquiry_created_before: filter.inquiryCreatedBefore,
    inquiry_created_after: filter.inquiryCreatedAfter,
    inquiry_completed_before: filter.inquiryCompletedBefore,
    inquiry_completed_after: filter.inquiryCompletedAfter,
    inquiry_state: filter.inquiryState,
    inquiry_answer: filter.inquiryAnswer,
    is_suspended: filter.suspended,
    is_bab: filter.bab,
    ...(macroCondition(getOwnConfig().application === "ur")
      ? {
          location: filter.municipality,
        }
      : {}),
  };
  const specificFilters = {
    "camac-ng": {
      location: filter.municipality,
      intent_sz: filter.intent,
      address_sz: filter.address,
      plot_egrid_sz: filter.parcel_egrid,
      plot_number_sz: filter.parcel_property_number,
      builder_sz: filter.builder,
      landowner_sz: filter.landowner,
      applicant_sz: filter.applicant,
      submit_date_after_sz: filter.submitDateAfter,
      submit_date_before_sz: filter.submitDateBefore,
      form_name_versioned: filter.type,
      objection_received: filter.objectionReceived,
      construction_zone_location_sz: filter.constructionZoneLocation,
      identifier: filter.instanceIdentifier || "",
      keyword_search: filter.keywordSearch,
    },
    caluma: {
      // BE-specific
      is_modification: filter.modification,
      decision_date_before: filter.decisionDateBefore,
      decision_date_after: filter.decisionDateAfter,
      // UR-specific
      circulation_state: hasActivation
        ? caseTableConfig.activeCirculationStates
        : null,
      has_pending_billing_entry: hasPendingBillingEntry,
      has_pending_sanction: hasPendingSanction,
      pending_sanctions_control_instance:
        filter.pendingSanctionsControlInstance,
      has_pending_sanctions_assigned_to_service:
        filter.hasPendingSanctionsAssignedToService,
      with_cantonal_participation: filter.withCantonalParticipation,
      oereb_legal_state: filter.legalStateOereb,
      // SZ-specific
      caluma_keyword_search: filter.calumaKeywordSearch,
    },
  };
  return {
    ...commonFilters,
    ...specificFilters[casesBackend],
  };
}
