import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { INQUIRY_STATUS } from "@projectcaluma/ember-distribution/config";

const DISTRIBUTION_NEW_INQUIRY_GROUP_TYPES_MAPPING = {
  roles: {
    3: ["suggestions", "Baugesuchszentrale", "Fachstellen Gemeinden"], // Gemeinde
    8: ["suggestions", "Baugesuchszentrale", "Fachstellen Gemeinden"], // Gemeinde Sachbearbeiter
    11: ["suggestions", "Gemeinde", "Baugesuchszentrale"], // Fachstelle Leitbehörde
    5: ["suggestions", "subservice"], // Fachstelle
  },
  groups: {
    7: ["suggestions", "Externe Fachstellen", "Fachstellen"], // Baugesuchszentrale
  },
};

export default class CustomCalumaOptionsService extends CalumaOptionsService {
  @service shoebox;
  @service store;

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

  async fetchTypedGroups(types, search) {
    return await types.reduce(async (typed, type) => {
      let filters =
        type === "subservice"
          ? { service_parent: this.shoebox.content.serviceId }
          : { service_group_name: type, has_parent: false };

      if (macroCondition(getOwnConfig().application === "sz")) {
        filters = { ...filters, available_in_distribution: true };
      }

      const result = await this.store.query("public-service", {
        search,
        ...filters,
      });

      return { ...(await typed), [type]: result };
    }, Promise.resolve({}));
  }

  get distribution() {
    if (macroCondition(getOwnConfig().application === "be")) {
      return {
        ui: { stack: true, small: true },
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
              },
            },
            statusMapping: {
              "inquiry-answer-status-positive": INQUIRY_STATUS.POSITIVE,
              "inquiry-answer-status-negative": INQUIRY_STATUS.NEGATIVE,
              "inquiry-answer-status-claim": INQUIRY_STATUS.NEEDS_INTERACTION,
              "inquiry-answer-status-not-involved": INQUIRY_STATUS.POSITIVE,
              "inquiry-answer-status-obligated": INQUIRY_STATUS.NEGATIVE,
              "inquiry-answer-status-not-obligated": INQUIRY_STATUS.POSITIVE,
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
      };
    } else if (macroCondition(getOwnConfig().application === "sz")) {
      const config = {
        inquiry: {
          answer: {
            buttons: {
              "fill-inquiry": {
                color: "primary",
                label: "distribution.release-for-review",
              },
              "check-inquiry": {
                color: "primary",
                label: "distribution.confirm",
              },
              "revise-inquiry": {
                color: "default",
                label: "distribution.revise",
              },
              "alter-inquiry": {
                color: "primary",
                label: "distribution.release-adjustment-for-review",
              },
            },
            statusMapping: {
              "inquiry-answer-status-further-clarification":
                INQUIRY_STATUS.NEEDS_INTERACTION,
              "inquiry-answer-status-not-involved": INQUIRY_STATUS.POSITIVE,
              "inquiry-answer-status-claim": INQUIRY_STATUS.NEEDS_INTERACTION,
              "inquiry-answer-status-legal-hearing":
                INQUIRY_STATUS.NEEDS_INTERACTION,
              "inquiry-answer-status-claim-legal-hearing":
                INQUIRY_STATUS.NEEDS_INTERACTION,
              "inquiry-answer-status-final": INQUIRY_STATUS.POSITIVE,
              "inquiry-answer-status-opposition": INQUIRY_STATUS.NEGATIVE,
              "inquiry-answer-status-inspection": INQUIRY_STATUS.POSITIVE,
            },
          },
        },
        new: {
          types: {
            "Externe Fachstellen": {
              label: "distribution.external-services",
            },
            Fachstellen: {
              label: "distribution.services-sz",
            },
            subservice: {
              label: "distribution.subservices",
            },
            Gemeinde: {
              label: "distribution.municipalities",
            },
            Baugesuchszentrale: {
              label: "distribution.bgz",
            },
            "Fachstellen Gemeinden": {
              label: "distribution.municipal-services",
            },
          },
        },
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
