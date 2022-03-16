import getAnswer from "camac-ng/utils/get-answer";

const intentSlugs = ["voranfrage-vorhaben"];
export default {
  intentSlugs,
  intent: (document) => {
    return getAnswer(document, intentSlugs)?.node.stringValue;
  },
};
