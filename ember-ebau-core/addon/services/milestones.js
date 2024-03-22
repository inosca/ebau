import Service, { service } from "@ember/service";
import { trackedFunction } from "reactiveweb/function";

export default class MilestonesService extends Service {
  @service store;
  @service ebauModules;
  @service fetch;
  @service intl;

  milestones = trackedFunction(this, async () => {
    const response = await this.fetch.fetch(
      `/api/v1/instances/${this.ebauModules.instanceId}/milestones`,
      {
        headers: { accept: "application/json" },
      },
    );
    const json = await response.json();
    return json.sections[0].fields;
  });

  async getMilestone(milestoneSlug) {
    const fieldValue = (this.milestones.value ?? []).find(
      (field) => field.slug === milestoneSlug,
    )?.value;

    if (!fieldValue) {
      return null;
    }

    if (Array.isArray(fieldValue)) {
      return fieldValue
        .map((value) => this.intl.formatDate(new Date(value)))
        .join(", ");
    }
    if (fieldValue) {
      return this.intl.formatDate(new Date(fieldValue));
    }
  }
}
