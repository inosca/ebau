import { action } from "@ember/object";
import Component from "@glimmer/component";

// The component to display numbers with thousands separators
export default class CamacInputNumberSeparatorComponent extends Component {
  get displayValue() {
    return this.args.model?.value
      ? Number(this.args.model.value).toLocaleString("de-CH")
      : "";
  }

  @action
  onChange(e) {
    e.preventDefault();

    this.args["on-change"]?.(
      Number(e.target.value.replace(/,/, ".").replace(/[^0-9.]/g, ""))
    );
  }
}
