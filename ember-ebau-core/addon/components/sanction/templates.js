import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { findAll } from "ember-data-resources";
import { tracked } from "tracked-built-ins";

export default class SanctionsTemplatesComponent extends Component {
  @service store;
  @service ebauModules;
  @service router;
  @service notification;
  @service intl;

  selectedTemplates = tracked(Set);

  sanctionTemplatesQuery = findAll(this, "sanction-template", () => ({
    include: "assignedService",
  }));

  get isLoading() {
    return this.sanctionTemplatesQuery.isLoading;
  }

  get sanctionTemplates() {
    return this.sanctionTemplatesQuery.records;
  }

  get isValid() {
    return this.selectedTemplates.size > 0;
  }

  @action
  toggleTemplate(id) {
    this.selectedTemplates.delete(id) || this.selectedTemplates.add(id);
  }

  createSanctions = task(async () => {
    const instance = await this.store.findRecord(
      "instance",
      this.ebauModules.instanceId,
    );
    try {
      await Promise.all(
        [...this.selectedTemplates]
          .map((id) =>
            this.sanctionTemplates.find((template) => id === template.id),
          )
          .map((template) =>
            this.store.createRecord("sanction", {
              instance,
              name: template.name,
              description: template.description,
              controlStep: template.controlStep,
              assignedService: template.assignedService,
            }),
          )
          .map((sanction) => sanction.save()),
      );
      this.router.transitionTo(this.router.currentRoute.parent.name);
    } catch {
      this.notification.danger(
        this.intl.t("sanction.notification.error.createfromtemplate"),
      );
    }
  });
}
