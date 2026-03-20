import { service } from "@ember/service";
import Component from "@glimmer/component";
import { trackedFunction } from "reactiveweb/function";

export default class ConstructionMonitoringWorkItemAddressedComponent extends Component {
  @service store;
  @service ebauModules;

  instance = this.store.peekRecord("instance", this.ebauModules.instanceId);

  #addressedGroups = trackedFunction(this, async () => {
    const isActionableForControl =
      this.args.workItem.meta?.["is-actionable-for-control"];
    const addressedGroups = (this.args.workItem?.addressedGroups ?? []).filter(
      (group) => group !== "applicant",
    );

    // ignore group resolution when the workitem is not actionable for control.
    if (isActionableForControl === undefined) {
      return addressedGroups;
    }

    const activeServiceGroup = await this.instance.get(
      "activeService.serviceGroup",
    );
    const resolvedGroups = await Promise.all(
      addressedGroups.map(
        async (group) =>
          this.store.peekRecord("public-service", group, {
            include: "service_group",
          }) ??
          (await this.store.findRecord("public-service", group, {
            include: "service_group",
          })),
      ),
    );

    return resolvedGroups
      .filter((group) => {
        const serviceGroupSlug = group.get("serviceGroup.slug");

        // if the active service group has taken over control,
        // only show that group as addressed.
        if (isActionableForControl) {
          return serviceGroupSlug === activeServiceGroup.slug;
        }

        // otherwise show all, except the active service group,
        // since they are not actually addressed unless they would
        // take over control.
        return serviceGroupSlug !== activeServiceGroup.slug;
      })
      .map((group) => group.id);
  });

  get addressedGroups() {
    return this.#addressedGroups.value ?? [];
  }
}
