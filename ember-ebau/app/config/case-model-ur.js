import { getAnswer } from "ember-ebau-core/utils/get-answer";

const intentSlugs = [
  "proposal-description",
  "beschreibung-zu-mbv",
  "bezeichnung",
  "vorhaben-proposal-description",
  "veranstaltung-beschrieb",
  "beschreibung-reklame",
];

export default {
  intentSlugs,
  intent: (document) => {
    const answer = getAnswer(document, intentSlugs);

    return answer?.node.stringValue;
  },
};
