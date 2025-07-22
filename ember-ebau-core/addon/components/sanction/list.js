import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { confirm } from "ember-uikit";

export default class SanctionsListComponent extends Component {
  @service intl;
  @service notification;

  @action
  async delete(sanction) {
    try {
      if (
        await confirm(
          this.intl.t("sanction.confirm.delete", {
            name: sanction.name,
          }),
        )
      ) {
        await sanction.destroyRecord();
        this.notification.success(
          this.intl.t("sanction.notification.success.delete"),
        );
      }
    } catch {
      this.notification.danger(
        this.intl.t("sanction.notification.error.delete"),
      );
    }
  }
}
