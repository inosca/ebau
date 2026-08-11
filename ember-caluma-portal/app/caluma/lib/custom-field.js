import { service } from "@ember/service";
import Field from "@projectcaluma/ember-form/lib/field";
import { didCancel } from "ember-concurrency";
import { isApplication } from "ember-ebau-core/helpers/is-application";

export default class CustomField extends Field {
  @service eebaClient;

  /**
   * Override parent afterSave hook to perform a refresh after specific questions are saved.
   */
  async afterSave(response) {
    if (!isApplication("gr")) {
      return;
    }

    const { question } = response;
    try {
      await this.eebaClient.onSaveEebaRefresh.perform(this.document, question);
    } catch (e) {
      if (didCancel(e)) {
        return;
      }

      throw e;
    }
  }
}
