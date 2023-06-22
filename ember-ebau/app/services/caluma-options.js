import { getOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { INQUIRY_STATUS } from "@projectcaluma/ember-distribution/config";
import { cached } from "tracked-toolbox";

export default class CustomCalumaOptionsService extends CalumaOptionsService {
  @service ebauModules;
  @service session;
  @service store;

  get currentGroupId() {
    return this.session.service.id;
  }

  get currentInstanceId() {
    return this.ebauModules.instanceId;
  }

  async _fetchIfNotCached(modelName, idFilter, identifiers) {
    const cachedIdentifiers = this.store
      .peekAll(modelName)
      .map((model) => model.id);

    const uncachedIdentifiers = identifiers.filter(
      (identifier) => !cachedIdentifiers.includes(String(identifier))
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

  @cached
  get distribution() {
    return {
      ui: { stack: false, small: false, readonly: this.session.isReadOnlyRole },
      inquiry: {
        answer: {
          infoQuestions: [
            "inquiry-answer-situation",
            "inquiry-answer-considerations",
            "inquiry-answer-assessment",
            "inquiry-answer-ancillary-clauses",
          ],
          buttons: {
            "fill-inquiry": {
              color: "primary",
              label: "distribution.send-answer",
              status: "caluma.distribution.answer.buttons.compose.status",
            },
          },
          statusMapping: {
            "inquiry-answer-status-positive": INQUIRY_STATUS.POSITIVE,
            "inquiry-answer-status-negative": INQUIRY_STATUS.NEGATIVE,
            "inquiry-answer-status-approved": INQUIRY_STATUS.POSITIVE,
            "inquiry-answer-status-rejected": INQUIRY_STATUS.NEGATIVE,
            "inquiry-answer-status-written-off": INQUIRY_STATUS.NEGATIVE,
          },
        },
      },
      new: {
        types: {
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
        },
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
}
