import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { INQUIRY_STATUS } from "@projectcaluma/ember-distribution/config";
import { cached } from "tracked-toolbox";

const DISTRIBUTION_NEW_INQUIRY_GROUP_TYPES_MAPPING = {
  roles: {
    3: ["suggestions", "Fachstellen Gemeinden"], // Gemeinde
    8: ["suggestions", "Fachstellen Gemeinden"], // Gemeinde Sachbearbeiter
    11: ["suggestions", "Gemeinde"], // Fachstelle Leitbehörde
    5: ["suggestions", "subservice"], // Fachstelle
  },
  groups: {
    7: ["suggestions", "Externe Fachstellen", "Fachstellen"], // Baugesuchszentrale
  },
};

export default class CustomCalumaOptionsService extends CalumaOptionsService {
  @service shoebox;
  @service store;
  @service fetch;

  get currentServiceId() {
    return this.shoebox.content.serviceId;
  }

  get currentGroupId() {
    return String(this.currentServiceId);
  }

  get currentInstanceId() {
    return this.shoebox.content.instanceId;
  }

  get currentRoleId() {
    return this.shoebox.content.roleId;
  }

  redirectToInstanceResource() {
    location.assign(
      `/index/redirect-to-instance-resource/instance-id/${this.currentInstanceId}`,
    );
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

  async fetchTypedGroups(types, search) {
    return await types.reduce(async (typed, type) => {
      let filters =
        type === "subservice"
          ? { service_parent: this.shoebox.content.serviceId }
          : type === "suggestions"
            ? { suggestion_for_instance: this.currentInstanceId }
            : { service_group_name: type, has_parent: false };

      if (macroCondition(getOwnConfig().application === "sz")) {
        filters = { ...filters, available_in_distribution: true };
      }

      const result = await this.store.query("public-service", {
        search,
        exclude_own_service: true,
        ...filters,
      });

      return { ...(await typed), [type]: result };
    }, Promise.resolve({}));
  }

  @cached
  get distribution() {
    const permissions = {
      completeDistribution: () => this.shoebox.isLeadRole,
      reopenDistribution: () => this.shoebox.isLeadRole,
      createInquiry: () => this.shoebox.isLeadRole,
      editInquiry: () => this.shoebox.isLeadRole,
      sendInquiry: () => this.shoebox.isLeadRole,
      withdrawInquiry: () => this.shoebox.isLeadRole,
      completeInquiryChildWorkItem: () => this.shoebox.isLeadRole,
      reopenInquiry: () => this.shoebox.isLeadRole,
      checkInquiries: () => this.shoebox.isLeadRole,
    };

    const hooks = {
      postCompleteDistribution: () => this.redirectToInstanceResource(),
    };

    if (macroCondition(getOwnConfig().application === "be")) {
      return {
        ui: { stack: true, small: true, readonly: this.shoebox.isReadOnlyRole },
        inquiry: {
          answer: {
            infoQuestions: [
              "inquiry-answer-statement",
              "inquiry-answer-ancillary-clauses",
            ],
            buttons: {
              "fill-inquiry": {
                color: "primary",
                label: "distribution.send-answer",
                status: "caluma.distribution.answer.buttons.compose.status",
                willCompleteInquiry: true,
              },
            },
            statusMapping: {
              "inquiry-answer-status-positive": INQUIRY_STATUS.POSITIVE,
              "inquiry-answer-status-negative": INQUIRY_STATUS.NEGATIVE,
              "inquiry-answer-status-claim": INQUIRY_STATUS.NEEDS_INTERACTION,
              "inquiry-answer-status-not-involved": INQUIRY_STATUS.POSITIVE,
              "inquiry-answer-status-obligated": INQUIRY_STATUS.NEGATIVE,
              "inquiry-answer-status-not-obligated": INQUIRY_STATUS.POSITIVE,
              "inquiry-answer-status-unknown": {
                icon: "question",
                color: "emphasis",
              },
            },
          },
        },
        new: {
          types: {
            district: {
              label: "distribution.districts",
            },
            municipality: {
              label: "distribution.municipalities",
            },
            service: {
              label: "distribution.services",
            },
            subservice: {
              label: "distribution.subservices",
            },
          },
        },
        permissions,
        hooks,
        inquiryReminderNotificationTemplateSlug:
          "05-meldung-fristuberschreitung-fachstelle",
      };
    } else if (macroCondition(getOwnConfig().application === "sz")) {
      const config = {
        ui: { readonly: this.shoebox.isReadOnlyRole },
        inquiry: {
          answer: {
            infoQuestions: [
              "inquiry-answer-request",
              "inquiry-answer-ancillary-clauses",
              "inquiry-answer-reason",
              "inquiry-answer-recommendation",
              "inquiry-answer-hint",
            ],
            buttons: {
              "fill-inquiry": {
                color: "primary",
                label: "distribution.release-for-review",
                status: "caluma.distribution.answer.buttons.compose.status",
              },
              "check-inquiry": {
                color: "primary",
                label: "distribution.confirm",
                status: {
                  label: "caluma.distribution.answer.buttons.confirm.status",
                  color: { addressed: "muted", controlling: "emphasis" },
                  icon: "user",
                },
                willCompleteInquiry: true,
              },
              "revise-inquiry": {
                color: "default",
                label: "distribution.revise",
              },
              "alter-inquiry": {
                color: "primary",
                label: "distribution.release-adjustment-for-review",
                status: "caluma.distribution.answer.buttons.adjust.status",
              },
            },
            statusMapping: {
              "inquiry-answer-status-further-clarification": {
                icon: "search",
                color: "warning",
              },
              "inquiry-answer-status-not-involved": INQUIRY_STATUS.POSITIVE,
              "inquiry-answer-status-claim": {
                icon: "file",
                color: "warning",
              },
              "inquiry-answer-status-legal-hearing": {
                icon: "file-text",
                color: "danger",
              },
              "inquiry-answer-status-claim-legal-hearing": {
                icon: "copy",
                color: "danger",
              },
              "inquiry-answer-status-final": INQUIRY_STATUS.POSITIVE,
              "inquiry-answer-status-opposition": {
                icon: "bolt",
                color: "danger",
              },
              "inquiry-answer-status-inspection": {
                icon: "camera",
                color: "warning",
              },
              "inquiry-answer-status-interim-report": {
                icon: "future",
                color: "warning",
              },
            },
            details: (inquiry) => {
              const releasedForReviewWorkItem =
                inquiry.childCase.workItems.edges
                  .map((workItem) => workItem.node)
                  .filter(
                    (workItem) =>
                      ["fill-inquiry", "alter-inquiry"].includes(
                        workItem.task.slug,
                      ) && workItem.status === "COMPLETED",
                  )
                  .sort((a, b) => a.closedAt - b.closedAt)
                  .reverse()[0];

              return [
                {
                  label: "caluma.distribution.inquiry.sent-at",
                  value: inquiry.childCase?.createdAt,
                  type: "date",
                },
                {
                  label: "caluma.distribution.inquiry.assigned-user",
                  value: inquiry.assignedUsers,
                  type: "user",
                },
                {
                  label: "distribution.released-for-review",
                  value: releasedForReviewWorkItem?.closedAt,
                  type: "date",
                },
                {
                  label: "distribution.released-for-review-by",
                  value: releasedForReviewWorkItem?.closedByUser,
                  type: "user",
                },
                {
                  label: "caluma.distribution.inquiry.closed-at",
                  value: inquiry.closedAt,
                  type: "date",
                },
                {
                  label: "distribution.closed-by",
                  value: inquiry.closedByUser,
                  type: "user",
                },
              ];
            },
          },
        },
        new: {
          types: {
            "Externe Fachstellen": {
              label: "distribution.external-services",
            },
            Fachstellen: {
              label: "distribution.services",
            },
            subservice: {
              label: "distribution.subservices",
            },
            Gemeinde: {
              label: "distribution.municipalities",
            },
            "Fachstellen Gemeinden": {
              label: "distribution.municipal-services",
            },
          },
        },
        permissions: {
          ...permissions,
          completeInquiryChildWorkItem: (_, task) =>
            !["check-inquiry", "revise-inquiry"].includes(task) ||
            this.shoebox.isLeadRole,
        },
        hooks,
        inquiryReminderNotificationTemplateSlug: "fristueberschreitung",
      };

      const activeTypes =
        DISTRIBUTION_NEW_INQUIRY_GROUP_TYPES_MAPPING.groups[
          this.currentGroupId
        ] ??
        DISTRIBUTION_NEW_INQUIRY_GROUP_TYPES_MAPPING.roles[this.currentRoleId];

      return {
        ...config,
        new: {
          types: Object.keys(config.new.types)
            .filter((key) => (activeTypes ? activeTypes.includes(key) : false))
            .reduce((obj, key) => {
              obj[key] = config.new.types[key];
              return obj;
            }, {}),
        },
      };
    }

    return {};
  }
}
