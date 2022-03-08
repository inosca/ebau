import { inject as service } from "@ember/service";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { INQUIRY_STATUS } from "@projectcaluma/ember-distribution/config";

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

  async resolveGroups(identifiers) {
    const cachedIdentifiers = this.store
      .peekAll("public-service")
      .map((service) => service.id);

    const uncachedIdentifiers = identifiers.filter(
      (identifier) => !cachedIdentifiers.includes(String(identifier))
    );

    if (uncachedIdentifiers.length) {
      await this.store.query("public-service", {
        service_id: String(uncachedIdentifiers),
      });
    }

    return this.store.peekAll("public-service");
  }

  async fetchTypedGroups(types, search) {
    return await types.reduce(async (typed, type) => {
      const filters =
        type === "subservice"
          ? { service_parent: this.shoebox.content.serviceId }
          : { service_group_name: type, has_parent: false };

      const result = await this.store.query("public-service", {
        search,
        ...filters,
      });

      return { ...(await typed), [type]: result };
    }, Promise.resolve({}));
  }

  distribution = {
    ui: { stack: true, small: true },
    inquiry: {
      answer: {
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
}
