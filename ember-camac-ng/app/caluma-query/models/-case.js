import { inject as service } from "@ember/service";
import CaseModel from "@projectcaluma/ember-core/caluma-query/models/case";

import caseModelConfig from "camac-ng/config/case-model";
import getAnswer from "camac-ng/utils/get-answer";

export default class CustomCaseBaseModel extends CaseModel {
  @service store;
  @service intl;

  get instanceId() {
    return this.raw.meta["camac-instance-id"];
  }

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get submitDate() {
    const submitDate = this.raw.meta["submit-date"]?.split("T")[0];

    return submitDate
      ? this.intl.formatDate(submitDate, {
          format: "date",
        })
      : null;
  }

  get intent() {
    return getAnswer(this.raw.document, caseModelConfig.intentSlugs)?.node
      .stringValue;
  }
}
