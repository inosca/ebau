import { helper } from "@ember/component/helper";
import { get, getWithDefault } from "@ember/object";

export const formTypes = {
  "vorabklaerung-einfach": "Einfache Vorabklärung",
  "vorabklaerung-vollstaendig": "Vollständige Vorabklärung",
  baugesuch: "Baugesuch",
  projektaenderung: "Projektänderung",
  "generelles-baugesuch": "Generelles Baugesuch",
  "baugesuch-mit-uvp": "Baugesuch mit UVP"
};

export function instanceType([document]) {
  const formTypeAnswer = getWithDefault(document, "answers.edges", []).find(
    edge => edge.node.question.slug === "formulartyp"
  );
  const slug = formTypeAnswer
    ? formTypeAnswer.node.stringValue
    : get(document, "form.name");
  return formTypes[slug] || slug;
}

export default helper(instanceType);
