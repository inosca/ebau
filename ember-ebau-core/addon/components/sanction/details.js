import { action } from "@ember/object";
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

  async submit(changeset, action) {
    if (action === "control") {
      if (
        !(await confirm(
          this.intl.t("sanction.confirm.control", { name: changeset.name }),
        ))
      ) {
        return;
      }
    }
    try {
      await this.fetch.fetch(
        `/api/v1/sanctions/${this.args.sanction.id}/${action}`,
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
        this.intl.t(`sanction.notification.success.${action}`),
      );
      if (action === "control") {
        this.router.transitionTo(
          this.ebauModules.resolveModuleRoute("sanctions", "index"),
        );
      }
    } catch {
      this.notification.danger(
        this.intl.t(`sanction.notification.error.${action}`),
      );
    }
  }

  annotate = task({ drop: true }, async (changeset) => {
    await this.submit(changeset, "annotate");
  });

  control = task({ drop: true }, async (changeset) => {
    await this.submit(changeset, "control");
  });

  @action
  back(changeset) {
    changeset.data.rollbackAttributes();
    this.router.transitionTo(
      this.ebauModules.resolveModuleRoute("sanctions", "index"),
    );
  }
}
