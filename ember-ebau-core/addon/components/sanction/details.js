import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { confirm } from "ember-uikit";

export default class SanctionsDetailsComponent extends Component {
  validations = {};

  @service ebauModules;
  @service fetch;
  @service router;
  @service notification;
  @service intl;

  submit = task({ drop: true }, async (changeset) => {
    if (
      !(await confirm(
        this.intl.t("sanction.confirm.control", { name: changeset.name }),
      ))
    ) {
      return;
    }
    try {
      await this.fetch.fetch(
        `/api/v1/sanctions/${this.args.sanction.id}/control`,
        {
          method: "POST",
          body: JSON.stringify({
            data: {
              type: "sanctions",
              id: `${this.args.sanction.id}`,
              attributes: {
                control_notes: changeset.controlNotes,
              },
            },
          }),
        },
      );
      this.notification.success(
        this.intl.t("sanction.notification.success.control"),
      );
      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("sanctions", "index"),
      );
    } catch {
      this.notification.danger(
        this.intl.t("sanction.notification.error.control"),
      );
    }
  });
}
