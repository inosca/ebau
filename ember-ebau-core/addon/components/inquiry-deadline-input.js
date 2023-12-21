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
    if (!this.serviceGroupSlugs.value) {
      return false;
    }
    return (this.serviceGroupSlugs.value || []).every((sg) =>
      specialServiceGroups.includes(sg),
    );
  }

  get _showHint() {
    return (this.serviceGroupSlugs.value || []).find((sg) =>
      specialServiceGroups.includes(sg),
    );
  }

  serviceGroupSlugs = trackedFunction(this, async () => {
    await Promise.resolve();

    const services = await this.store.query("service", {
      service_id: this.args?.context?.selectedGroups.toString(),
      include: "service_group",
    });
    const serviceGroupSlugs = services.map((service) => {
      return service.serviceGroup.get("slug");
    });
    return serviceGroupSlugs;
  });
}
