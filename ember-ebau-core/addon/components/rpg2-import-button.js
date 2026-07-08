import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";

export default class Rpg2ImportButtonComponent extends Component {
  @service intl;
  @service notification;
  @service fetch;

  @tracked data = {};
  @tracked showModal = false;

  get hasData() {
    return Object.keys(this.data).length > 0;
  }

  getData = dropTask(async () => {
    if (this.args.disabled) return;

    try {
      const response = await this.fetch.fetch(
        `/api/v1/instances/${this.args.context.instanceId}/rpg2-data`,
        { headers: { accept: "application/json" } },
      );

      if (!response.ok) {
        throw new Error(response.statusText);
      }

      const { data } = await response.json();
      this.data = data;
      this.showModal = true;
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("rpg2-import-button.preview-error"));
    }
  });

  applyData = dropTask(async () => {
    try {
      const response = await this.fetch.fetch(
        `/api/v1/instances/${this.args.context.instanceId}/rpg2-apply`,
        {
          method: "POST",
          headers: {
            accept: "application/json",
          },
        },
      );

      if (!response.ok) {
        throw new Error(response.statusText);
      }

      const { questions } = await response.json();

      this.showModal = false;

      await Promise.all(
        questions.map((slug) =>
          this.args.field.document
            .findField(slug)
            ?.refreshAnswer.linked()
            .perform(),
        ),
      );

      this.notification.success(this.intl.t("rpg2-import-button.success"));
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("rpg2-import-button.apply-error"));
    }
  });
}
