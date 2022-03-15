import { macroCondition, getOwnConfig } from "@embroider/macros";

import getAnswer from "camac-ng/utils/get-answer";

let config;
if (macroCondition(getOwnConfig().canton === "ur")) {
  config = {
    intent: (document) => {
      const answer = getAnswer(document, [
        "proposal-description",
        "beschreibung-zu-mbv",
        "bezeichnung",
        "vorhaben-proposal-description",
        "veranstaltung-beschrieb",
        "reklamen",
      ]);

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
  config = {
    intent: (document) => {
      return getAnswer(document, "voranfrage-vorhaben")?.node.stringValue;
    },
  };
}
export default config;
