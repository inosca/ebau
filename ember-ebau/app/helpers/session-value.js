import Helper from "@ember/component/helper";
import { get } from "@ember/object";
import { service } from "@ember/service";

export default class SessionValue extends Helper {
  @service session;

  compute([valuePath]) {
    return get(this.session, valuePath);
  }
}
