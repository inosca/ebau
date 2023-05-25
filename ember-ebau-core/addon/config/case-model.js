import { getOwnConfig, macroCondition } from "@embroider/macros";

import { getAnswer } from "ember-ebau-core/utils/get-answer";

let intentSlugs;
if (macroCondition(getOwnConfig().application === "ur")) {
  intentSlugs = [
    "proposal-description",
    "beschreibung-zu-mbv",
    "bezeichnung",
    "vorhaben-proposal-description",
    "veranstaltung-beschrieb",
    "beschreibung-reklame",
  ];
} else if (macroCondition(getOwnConfig().application === "sz")) {
  intentSlugs = ["voranfrage-vorhaben"];
} else {
  intentSlugs = ["beschreibung-bauvorhaben"];
}

export default {
  intentSlugs,
  intent: (document) => {
    const answer = getAnswer(document, intentSlugs);

    return answer?.node.stringValue;
  },
};
