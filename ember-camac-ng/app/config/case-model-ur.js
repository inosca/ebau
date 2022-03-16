import getAnswer from "camac-ng/utils/get-answer";

const intentSlugs = [
  "proposal-description",
  "beschreibung-zu-mbv",
  "bezeichnung",
  "vorhaben-proposal-description",
  "veranstaltung-beschrieb",
  "reklamen",
];

export default {
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
