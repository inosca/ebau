import Controller from "@ember/controller";
import { service } from "@ember/service";
import { validateFormat } from "ember-changeset-validations/validators";
import { task } from "ember-concurrency";

const validatePhone = validateFormat({
  type: "phone",
  // This regex is copied from caluma to make sure we use the same validation as
  // in the caluma forms
  regex: /^[\s/.()-]*(?:\+|0|00)(?:[\s/.()-]*\d[\s/.()-]*){6,20}$/,
  allowBlank: true,
});

export default class ProfileController extends Controller {
  validations = {
    phone: validatePhone,
    mobile: validatePhone,
  };

  @service intl;
  @service store;
  @service fetch;
  @service session;
  @service notification;

  save = task({ drop: true }, async (changeset) => {
    try {
      const response = await this.fetch.fetch("/api/v1/me", {
        method: "PATCH",
        body: JSON.stringify({
          data: {
            id: changeset.data.id,
            type: "users",
            attributes: changeset.change,
          },
        }),
      });

      this.store.pushPayload(await response.json());

      this.notification.success(this.intl.t("profile.success"));
    } catch {
      this.notification.danger(this.intl.t("profile.error"));
    }
  });
}
