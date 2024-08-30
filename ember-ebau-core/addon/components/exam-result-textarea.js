import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";

export default class ExamResultTextareaComponent extends Component {
  @service intl;

  #textarea = null;

  @action
  registerTextarea(element) {
    this.#textarea = element.querySelector("textarea");
  }

  @action
  collectResults(e) {
    e.preventDefault();

    const affectedFields = this.args.field.document.fields.filter(
      (f) =>
        f.questionType === "MultipleChoiceQuestion" &&
        f.selected.some((o) => o.slug === `${f.question.slug}-nachforderung`),
    );
    const labels = affectedFields
      .map((f) => `- ${f.question.raw.label}`)
      .join("\n");

    const current = this.#textarea.value;
    let text = `${this.intl.t("exam-results-textarea.additional-demands")}:\n\n${labels}`;

    if (current) {
      text = `${current}\n\n${text}`;
    }

    this.#textarea.value = text;
    this.#textarea.dispatchEvent(new Event("input"));
  }
}
