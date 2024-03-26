import { inject as service } from "@ember/service";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { INQUIRY_STATUS } from "@projectcaluma/ember-distribution/config";
import { cantonAware } from "ember-ebau-core/decorators";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import { cached } from "tracked-toolbox";

export default class CustomCalumaOptionsService extends CalumaOptionsService {
  @service ebauModules;
  @service session;
  @service store;
  @service fetch;

  alwaysUseNumberSeparatorWidget = hasFeature(
    "caluma.alwaysUseNumberSeparatorWidget",
  );

  get currentGroupId() {
    return this.session.service?.id;
  }

  get currentInstanceId() {
    return this.ebauModules.instanceId;
  }

  get isAuthority() {
    if (!this.currentInstanceId) {
      return false;
    }

    const instance = this.store.peekRecord("instance", this.currentInstanceId);
    const authorityId = parseInt(instance?.belongsTo("activeService").id());

    return authorityId === parseInt(this.currentGroupId);
  }

  async _fetchIfNotCached(modelName, idFilter, identifiers) {
    const cachedIdentifiers = this.store
      .peekAll(modelName)
      .map((model) => model.id);

    const uncachedIdentifiers = identifiers.filter(
      (identifier) => !cachedIdentifiers.includes(String(identifier)),
    );

    if (uncachedIdentifiers.length) {
      await this.store.query(modelName, {
        [idFilter]: String(uncachedIdentifiers),
      });
    }

    return this.store.peekAll(modelName);
  }

  resolveUsers(identifiers) {
    return this._fetchIfNotCached("public-user", "username", identifiers);
  }

  resolveGroups(identifiers) {
    return this._fetchIfNotCached("public-service", "service_id", identifiers);
  }

  @cantonAware
  static distributionInfoQuestions = [];
  static distributionInfoQuestionsGR = [
    "inquiry-answer-situation",
    "inquiry-answer-considerations",
    "inquiry-answer-assessment",
    "inquiry-answer-ancillary-clauses",
  ];
  static distributionInfoQuestionsSO = [
    "inquiry-answer-positive-assessments",
    "inquiry-answer-negative-assessments",
    "inquiry-answer-rejection-additional-demand",
    "inquiry-answer-objections",
    "inquiry-answer-notices-for-applicant",
    "inquiry-answer-notices-for-authority",
    "inquiry-answer-notices-for-authority-arp",
    "inquiry-answer-forward",
  ];

  @cantonAware
  static distributionStatusMapping = {};
  static distributionStatusMappingGR = {
    "inquiry-answer-status-positive": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-negative": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-approved": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-rejected": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-written-off": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-claim": INQUIRY_STATUS.NEEDS_INTERACTION,
    "inquiry-answer-status-not-involved": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-following": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-renounced": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-unknown": {
      icon: "question",
      color: "emphasis",
    },
  };
  static distributionStatusMappingSO = {
    "inquiry-answer-status-positive": INQUIRY_STATUS.POSITIVE,
    "inquiry-answer-status-negative": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-additional-demand": INQUIRY_STATUS.NEEDS_INTERACTION,
    "inquiry-answer-status-rejection": INQUIRY_STATUS.NEGATIVE,
    "inquiry-answer-status-no-comment": INQUIRY_STATUS.POSITIVE,
  };

  @cantonAware
  get distributionServiceGroups() {
    return {};
  }

  get distributionServiceGroupsGR() {
    return {
      "authority-bab": {
        label: "distribution.authority-bab",
      },
      service: {
        label: "distribution.services",
      },
      municipality: {
        label: "distribution.municipalities",
      },
      subservice: {
        label: "distribution.subservices",
      },
    };
  }

  get distributionServiceGroupsSO() {
    if (!this.currentInstanceId) {
      return {};
    }

    const fullConfig = {
      municipality: {
        label: "distribution.municipalities",
      },
      "service-cantonal": {
        label: "distribution.services-cantonal",
      },
      "service-extra-cantonal": {
        label: "distribution.services-extra-cantonal",
      },
      subservice: {
        label: "distribution.subservices",
      },
    };

    if (this.session.rolePermission === "service") {
      Reflect.deleteProperty(fullConfig, "municipality");
    }

    if (!this.isAuthority) {
      fullConfig.suggestions = { disabled: true };
    }

    if (this.session.rolePermission === "municipality" && !this.isAuthority) {
      Reflect.deleteProperty(fullConfig, "municipality");
      Reflect.deleteProperty(fullConfig, "service-cantonal");
      Reflect.deleteProperty(fullConfig, "service-extra-cantonal");
    }

    return fullConfig;
  }

  @cantonAware
  get distributionDefaultServiceGroups() {
    return ["suggestions"];
  }

  get distributionDefaultServiceGroupsSO() {
    if (this.isAuthority) {
      return ["suggestions"];
    }

    return ["subservice"];
  }

  @cached
  get distribution() {
    return {
      ui: { readonly: this.session.isReadOnlyRole },
      inquiry: {
        answer: {
          infoQuestions: CustomCalumaOptionsService.distributionInfoQuestions,
          buttons: {
            "fill-inquiry": {
              color: "primary",
              label: "distribution.send-answer",
              status: "caluma.distribution.answer.buttons.compose.status",
              willCompleteInquiry: true,
            },
          },
          statusMapping: CustomCalumaOptionsService.distributionStatusMapping,
        },
      },
      new: {
        types: this.distributionServiceGroups,
        defaultTypes: this.distributionDefaultServiceGroups,
      },
      permissions: {
        completeDistribution: () => this.session.isLeadRole,
        reopenDistribution: () => this.session.isLeadRole,
        sendInquiry: () => this.session.isLeadRole,
        withdrawInquiry: () => this.session.isLeadRole,
        completeInquiryChildWorkItem: () => this.session.isLeadRole,
        reopenInquiry: () => this.session.isLeadRole,
        checkInquiries: () => this.session.isLeadRole,
      },
      hooks: {
        postCompleteDistribution: () => this.ebauModules.redirectToWorkItems(),
      },
      inquiryReminderNotificationTemplateSlug: "inquiry-reminder",
    };
  }

  async fetchTypedGroups(types, search) {
    return await types.reduce(async (typed, type) => {
      const filters =
        type === "subservice"
          ? { service_parent: this.ebauModules.serviceId }
          : type === "suggestions"
            ? { suggestion_for_instance: this.currentInstanceId }
            : { service_group_name: type, has_parent: false };

      const result = await this.store.query("public-service", {
        search,
        exclude_own_service: true,
        ...filters,
      });

      return { ...(await typed), [type]: result };
    }, Promise.resolve({}));
  }

  async sendReminderDistributionInquiry(inquiryId) {
    if (!this.distribution.inquiryReminderNotificationTemplateSlug) {
      return;
    }

    await this.fetch.fetch(`/api/v1/notification-templates/sendmail`, {
      method: "POST",
      headers: {
        accept: "application/vnd.api+json",
        "content-type": "application/vnd.api+json",
      },
      body: JSON.stringify({
        data: {
          type: "notification-template-sendmails",
          attributes: {
            "template-slug":
              this.distribution.inquiryReminderNotificationTemplateSlug,
            "recipient-types": ["inquiry_addressed"],
          },
          relationships: {
            instance: {
              data: { type: "instances", id: this.currentInstanceId },
            },
            inquiry: { data: { type: "work-items", id: inquiryId } },
          },
        },
      }),
    });
  }
}
