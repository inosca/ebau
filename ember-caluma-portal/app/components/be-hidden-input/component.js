import Component from "@ember/component";

export default class BeHiddenInputComponent extends Component {
  tagName = "input";
  attributeBindings = ["type"];
  type = "hidden";
}
