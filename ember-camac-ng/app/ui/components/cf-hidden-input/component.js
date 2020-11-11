import Component from "@glimmer/component";

export default class BeHiddenInputComponent extends Component {
  tagName = "input";
  attributeBindings = ["type"];
  type = "hidden";
}
