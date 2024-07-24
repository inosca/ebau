import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

export default class KeycloakProfileApplyButtonComponent extends Component {
  @service intl;
  @service notification;
  @service fetch;

  applyData = dropTask(async () => {
    const response = await this.fetch.fetch(`/api/v1/keycloak-apply`, {
      method: "POST",
      body: JSON.stringify({
        document: this.args.field.document.uuid,
      }),
      headers: {
        "content-type": "application/json",
        accept: "application/json",
      },
    });

    const { questions } = await response.json();

    await Promise.all(
      questions.map((slug) =>
        this.args.field.document
          .findField(slug)
          ?.refreshAnswer.linked()
          .perform(),
      ),
    );

    this.notification.success(
      this.intl.t("keycloak-profile-apply-button.success"),
    );
  });
}
