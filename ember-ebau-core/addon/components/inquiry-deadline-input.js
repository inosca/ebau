import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import config from "@projectcaluma/ember-distribution/config";
import { DateTime } from "luxon";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";

const specialServiceGroups = mainConfig.customDeadlineServiceGroupSlugs;
export default class InquiryDeadlineInputComponent extends Component {
  @service store;

  @config distributionConfig;

  @tracked disabled = false;

  get isBulk() {
    return this.args.field.document.uuid.startsWith("inquiry-document-");
  }

  get serviceIds() {
    return this.isBulk
      ? this.args.context.selectedGroups
      : this.args.context?.inquiry.addressedGroups;
  }

  get isDisabled() {
    if (this.args.disabled) {
      return true;
    }

    const slugs = this.serviceGroupSlugs.value ?? [];
    return !slugs.length
      ? false
      : slugs.every((sg) => specialServiceGroups.includes(sg));
  }

  get showHint() {
    const slugs = this.serviceGroupSlugs.value ?? [];
    return slugs.some((sg) => specialServiceGroups.includes(sg));
  }

  serviceGroupSlugs = trackedFunction(this, async () => {
    await Promise.resolve();

    if (!this.serviceIds) {
      return [];
    }

    const services = await this.store.query("service", {
      service_id: this.serviceIds.toString(),
      include: "service_group",
    });

    return services.map((service) => {
      return service.serviceGroup.get("slug");
    });
  });

  get isHidden() {
    return this.isBulk && this.args.field.value === "0000-01-01";
  }

  get rules() {
    if (!this.isBulk) {
      return [];
    }

    const rules = this.store.peekAll("distribution-deadline-rule");
    const defaultDeadline = DateTime.now()
      .plus({ days: this.distributionConfig.new.defaultDeadlineLeadTime })
      .toISODate();

    return this.serviceIds.map((id) => {
      const rule = rules.find((rule) => rule.get("targetService.id") === id);
      const service = this.store.peekRecord("public-service", id);

      return {
        name: service.name,
        deadline: rule?.deadline ?? defaultDeadline,
      };
    });
  }
}
