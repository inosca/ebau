import CustomCaseModel from "ember-ebau-core/caluma-query/models/case";

export function initialize(application) {
  application.register("caluma-query-model:case", CustomCaseModel);
}

export default {
  initialize,
};
