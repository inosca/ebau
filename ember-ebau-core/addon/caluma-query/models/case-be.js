import CustomCaseBaseModel from "ember-ebau-core/caluma-query/models/-case";

export default class CustomCaseModel extends CustomCaseBaseModel {
  get decision() {
    return this.instance?.decision;
  }

  get decisionDate() {
    const decisionDate = this.instance?.decisionDate;

    return decisionDate
      ? this.intl.formatDate(decisionDate, { format: "date" })
      : null;
  }

  get instanceState() {
    const state = super.instanceState;

    if (this.decision) {
      return `${state} (${this.decision})`;
    }

    return state;
  }
}
