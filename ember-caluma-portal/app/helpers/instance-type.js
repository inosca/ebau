import { helper } from "@ember/component/helper";
import { get } from "@ember/object";

export const formTypes = {
  "vorabklaerung-einfach": "Einfache Vorabklärung",
  "vorabklaerung-vollstaendig": "Vollständige Vorabklärung",
  baugesuch: "Baugesuch",
  projektaenderung: "Projektänderung",
  "generelles-baugesuch": "Generelles Baugesuch",
  "baugesuch-mit-uvp": "Baugesuch mit UVP"
};

export function instanceType([document]) {
  const slug =
    get(document, "answers.edges.firstObject.node.stringValue") ||
    get(document, "form.name");
  return formTypes[slug] || slug;
}

export default helper(instanceType);
