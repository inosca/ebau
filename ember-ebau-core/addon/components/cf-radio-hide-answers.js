import CfFieldInputRadioComponent from "@projectcaluma/ember-form/components/cf-field/input/radio";

/**
 * This custom radio component is used to hide answers (e.g. decision unknown)
 * So it can not be manually selected. If the radio is no longer changeable,
 * and the answer matches the answer, an alternative text is shown.
 */
export default class CfRadioHideAnswersComponent extends CfFieldInputRadioComponent {
  get visibleOptions() {
    const field = this.args.field;
    const options = field.options || [];
    const disabledManualAnswers =
      field.question?.raw?.meta?.hiddenAnswers || [];

    return options.filter(
      (option) => !disabledManualAnswers.includes(option.slug),
    );
  }

  get alternativeText() {
    const field = this.args.field;
    const disabledManualAnswers =
      field.question?.raw?.meta?.hiddenAnswers || [];
    const alternativeText = field.question?.raw?.meta?.alternativeText || {};
    const answer = field.answer?.value || null;

    if (disabledManualAnswers.includes(answer)) {
      return alternativeText[answer] || null;
    }

    return null;
  }
}
