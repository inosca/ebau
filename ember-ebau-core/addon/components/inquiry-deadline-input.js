import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { trackedFunction } from "ember-resources/util/function";

import mainConfig from "ember-ebau-core/config/main";

const specialServiceGroups = mainConfig.customDeadlineServiceGroupSlugs;
export default class InquiryDeadlineInputComponent extends Component {
  @service store;

  @tracked disabled = false;

  get isDisabled() {
    const slugs = this.serviceGroupSlugs.value;
    if (!slugs || !slugs.length) {
      return false;
    }
    return slugs.every((sg) => specialServiceGroups.includes(sg));
  }

  get _showHint() {
    return (this.serviceGroupSlugs.value || []).find((sg) =>
      specialServiceGroups.includes(sg),
    );
  }

  serviceGroupSlugs = trackedFunction(this, async () => {
    await Promise.resolve();

    const serviceIds = this.args?.context?.selectedGroups;

    if (!serviceIds) {
      return [];
    }

    const services = await this.store.query("service", {
      service_id: serviceIds.toString(),
      include: "service_group",
    });
    return services.map((service) => {
      return service.serviceGroup.get("slug");
    });
  });
}
