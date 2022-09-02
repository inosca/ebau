import { getAnswer } from "ember-ebau-core/utils/get-answer";

const intentSlugs = ["voranfrage-vorhaben"];
export default {
  intentSlugs,
  intent: (document) => {
    return getAnswer(document, intentSlugs)?.node.stringValue;
  },
};
