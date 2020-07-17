import { A } from "@ember/array";
import Component from "@ember/component";

const CamacInputErrorComponent = Component.extend({
  error: A(),
});

CamacInputErrorComponent.reopenClass({
  positionalParams: ["error"],
});

export default CamacInputErrorComponent;
