import { inject as service } from "@ember/service";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";

export default class CustomCalumaOptionsService extends CalumaOptionsService {
  @service session;
  @service store;

  get currentGroupId() {
    return this.session.service.id;
  }

  async fetchTypedGroups(types, search) {
    return await types.reduce(async (typed, type) => {
      const filters =
        type === "subservice"
          ? { service_parent: this.shoebox.content.serviceId }
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
