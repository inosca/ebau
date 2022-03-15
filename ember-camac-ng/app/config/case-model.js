import { macroCondition, getOwnConfig } from "@embroider/macros";

import getAnswer from "camac-ng/utils/get-answer";

let config;
if (macroCondition(getOwnConfig().canton === "ur")) {
  const intentSlugs = [
    "proposal-description",
    "beschreibung-zu-mbv",
    "bezeichnung",
    "vorhaben-proposal-description",
    "veranstaltung-beschrieb",
    "reklamen",
  ];

  config = {
    intentSlugs,
    intent: (document) => {
      const answer = getAnswer(document, intentSlugs);

      if (answer?.node.question.slug === "reklamen") {
        const mapping = {
          "art-der-reklame-neue": "Neue Reklame",
          "art-der-reklame-aenderung": "Änderung bestehender Reklame",
        };
        return mapping[
          getAnswer(answer?.node.value[0], "art-der-reklame")?.node.stringValue
        ];
      }

      return answer?.node.stringValue;
    },
  };
}
if (macroCondition(getOwnConfig().canton === "be")) {
  config = {};
}
if (macroCondition(getOwnConfig().canton === "sz")) {
  const intentSlugs = ["voranfrage-vorhaben"];
  config = {
    intentSlugs,
    intent: (document) => {
      return getAnswer(document, intentSlugs)?.node.stringValue;
    },
  };
}
export default config;
