import Component from "@ember/component";

export default class BeDisabledInputComponent extends Component {
  tagName = "input";
  classNames = ["uk-input"];
  classNameBindings = ["forceDisabled:uk-disabled"];
  attributeBindings = [
    "forceDisabled:readonly",
    "field.pk:name",
    "field.pk:id",
    "field.answer.value:value",
  ];
  forceDisabled = true;
}
