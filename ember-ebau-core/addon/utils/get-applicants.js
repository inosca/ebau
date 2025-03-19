import { isEmpty } from "@ember/utils";

import mainConfig from "ember-ebau-core/config/main";
import {
  getAnswer,
  getAnswerDisplayValue,
} from "ember-ebau-core/utils/get-answer";

export function getNames(document, questionSlug) {
  const tableAnswer = getAnswer(document, questionSlug);
  const people = tableAnswer?.node.value ?? tableAnswer?.node.tableValue ?? [];

  const applicantNames = people.map((row) => {
    const firstName = getAnswerDisplayValue(
      row,
      mainConfig.answerSlugs.firstNameApplicant,
    );
    const lastName = getAnswerDisplayValue(
      row,
      mainConfig.answerSlugs.lastNameApplicant,
    );
    const fullName = [firstName, lastName]
      .filter(Boolean)
      .map((name) => name.trim())
      .join(" ");

    const juristicName =
      getAnswerDisplayValue(
        row,
        mainConfig.answerSlugs.juristicNameApplicant,
      )?.trim() ?? null;
    const isJuristic =
      getAnswerDisplayValue(row, mainConfig.answerSlugs.isJuristicApplicant) ===
      mainConfig.answerSlugs.isJuristicApplicantYes;

    if (isJuristic) {
      return isEmpty(juristicName) ? fullName : juristicName;
    }

    return fullName;
  });

  return applicantNames.filter(Boolean).join(", ");
}

export function getApplicants(document) {
  return getNames(document, mainConfig.answerSlugs.personalDataApplicant);
}
