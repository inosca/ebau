import mainConfig from "ember-ebau-core/config/main";
import {
  getAnswer,
  getAnswerDisplayValue,
} from "ember-ebau-core/utils/get-answer";

const { answerSlugs } = mainConfig;

export function getApplicants(document) {
  const applicants =
    getAnswer(document, answerSlugs.personalDataApplicant)?.node.value ?? [];

  const applicantNames = applicants.map((row) => {
    const firstName = getAnswerDisplayValue(
      row,
      answerSlugs.firstNameApplicant,
    );
    const lastName = getAnswerDisplayValue(row, answerSlugs.lastNameApplicant);
    const juristicName = getAnswerDisplayValue(
      row,
      answerSlugs.juristicNameApplicant,
    );

    return (
      juristicName?.trim() ??
      [firstName, lastName]
        .filter(Boolean)
        .map((name) => name.trim())
        .join(" ")
    );
  });

  return applicantNames.filter(Boolean).join(", ");
}
