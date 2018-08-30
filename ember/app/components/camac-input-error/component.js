import Component from "@ember/component";
import { A } from "@ember/array";

const CamacInputErrorComponent = Component.extend({
  error: A()
});

CamacInputErrorComponent.reopenClass({
  positionalParams: ["error"]
});

export default CamacInputErrorComponent;
