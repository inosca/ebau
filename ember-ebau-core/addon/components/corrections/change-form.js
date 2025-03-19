import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { confirm } from "ember-uikit";
import { trackedFunction } from "reactiveweb/function";
import { localCopy } from "tracked-toolbox";

export default class CorrectionsChangeForm extends Component {
  @service fetch;
  @service intl;
  @service notification;
  @service ebauModules;

  @localCopy("args.instance.calumaForm") form;
  @tracked showHint = false;

  availableForms = trackedFunction(this, async () => {
    const response = await this.fetch.fetch(
      `/api/v1/instances/${this.args.instance.id}/changeable-forms`,
    );
    const { data } = await response.json();

    return data;
  });

  @action
  setForm(event) {
    this.form = event.target.value;
  }

  save = task({ drop: true }, async (event) => {
    event.preventDefault();

    if (!(await confirm(this.intl.t("corrections.change-form.confirm")))) {
      return;
    }

    try {
      const response = await this.fetch.fetch(
        `/api/v1/instances/${this.args.instance.id}/change-form`,
        {
          method: "POST",
          body: JSON.stringify({
            data: {
              type: "instance-change-forms",
              id: this.args.instance.id,
              attributes: { form: this.form },
            },
          }),
        },
      );

      if (this.ebauModules.isLegacyApp) {
        // sadly we need this to have current data on the whole page
        location.reload();
      } else {
        await this.args.instance.reload();

        // If the response is 200 instead of 204, the form is not valid after
        // the change and the user needs to be made aware of it.
        this.showHint = response.status === 200;

        this.notification.success(
          this.intl.t("corrections.change-form.success"),
        );
      }
    } catch {
      this.notification.danger(this.intl.t("corrections.change-form.error"));
    }
  });
}
