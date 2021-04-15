import CustomField from "camac-ng/caluma/lib/custom-field";

export function initialize(application) {
  application.register("caluma-model:field", CustomField);
}

export default {
  initialize,
};
