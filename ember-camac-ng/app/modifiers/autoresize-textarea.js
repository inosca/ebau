import { modifier } from "ember-modifier";

export default modifier(function autoresizeTextarea(element) {
  const offset = element.offsetHeight - element.clientHeight;
  const setHeight = () => {
    element.style.height = "auto"; // Retract textarea
    element.style.height = `${element.scrollHeight + offset}px`; // Expand textarea
  };

  setHeight();
  element.addEventListener("input", setHeight);

  return () => element.removeEventListener("input", setHeight);
});
