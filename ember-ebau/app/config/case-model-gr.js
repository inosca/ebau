import { getAnswer } from "ember-ebau-core/utils/get-answer";

const intentSlugs = ["beschreibung-bauvorhaben"];
export default {
  intentSlugs,
  intent: (document) => {
    return getAnswer(document, intentSlugs)?.node.stringValue;
  },
};
