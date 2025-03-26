import { service } from "@ember/service";
import { getOwnConfig, macroCondition } from "@embroider/macros";
import Field from "@projectcaluma/ember-form/lib/field";
import { restartableTask } from "ember-concurrency";

export default class CustomField extends Field {
  @service eebaClient;

  /**
   * Override parent save to perform a refresh after specific questions are saved.
   *
   * We cannot use ember-concurrency `task()` because it needs to be the same
   * as the parent implementation.
   */
  @restartableTask
  *save() {
    const result = yield super.save.perform();
    if (macroCondition(getOwnConfig().application !== "gr")) {
      return result;
    }

    const { question } = result;

    yield this.eebaClient.onSaveEebaRefresh(this.document, question);

    return result;
  }
}
