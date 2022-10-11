import Helper from "@ember/component/helper";
import { get } from "@ember/object";
import { inject as service } from "@ember/service";

export default class SessionValue extends Helper {
  @service session;

  compute([valuePath]) {
    return get(this.session, valuePath);
  }
}
