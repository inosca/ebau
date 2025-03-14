import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { findAll } from "ember-data-resources";
import { confirm } from "ember-uikit";

export default class SanctionTemplatesListComponent extends Component {
  @service intl;
  @service notification;

  sanctionTemplatesQuery = findAll(this, "sanction-template", () => ({
    include: "assignedService",
  }));

  get sanctionTemplates() {
    return this.sanctionTemplatesQuery.records;
  }

  @action
  async delete(template) {
    try {
      if (
        await confirm(
          this.intl.t("sanctiontemplate.confirm.delete", {
            name: template.name,
          }),
        )
      ) {
        await template.destroyRecord();
        this.notification.success(
          this.intl.t("sanctiontemplate.notification.success.delete"),
        );
      }
    } catch {
      this.notification.danger(
        this.intl.t("sanctiontemplate.notification.error.delete"),
      );
    }
  }
}
