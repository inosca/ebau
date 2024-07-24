import Helper from "@ember/component/helper";
import { get } from "@ember/object";
import { service } from "@ember/service";

export default class ShoeboxValue extends Helper {
  @service shoebox;

  compute([valuePath]) {
    return get(this.shoebox.content, valuePath) ?? get(this.shoebox, valuePath);
  }
}
