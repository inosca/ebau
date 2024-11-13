import { isEmpty } from "@ember/utils";

import mainConfig from "ember-ebau-core/config/main";
import {
  getAnswer,
  getAnswerDisplayValue,
} from "ember-ebau-core/utils/get-answer";

export function getApplicants(document) {
  const applicants =
    getAnswer(document, mainConfig.answerSlugs.personalDataApplicant)?.node
      .value ?? [];

  const applicantNames = applicants.map((row) => {
    const firstName = getAnswerDisplayValue(
      row,
      mainConfig.answerSlugs.firstNameApplicant,
    );
    const lastName = getAnswerDisplayValue(
      row,
      mainConfig.answerSlugs.lastNameApplicant,
    );
    const juristicName =
      getAnswerDisplayValue(
        row,
        mainConfig.answerSlugs.juristicNameApplicant,
      )?.trim() ?? null;

    return isEmpty(juristicName)
      ? [firstName, lastName]
          .filter(Boolean)
          .map((name) => name.trim())
          .join(" ")
      : juristicName;
  });

  return applicantNames.filter(Boolean).join(", ");
}
