import CustomField from "caluma-portal/caluma/lib/custom-field";

export function initialize(application) {
  application.register("caluma-model:field", CustomField);
}

export default {
  initialize,
};
