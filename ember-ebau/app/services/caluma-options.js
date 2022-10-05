import { inject as service } from "@ember/service";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";

export default class CustomCalumaOptionsService extends CalumaOptionsService {
  @service session;

  get currentGroupId() {
    return this.session.group;
  }
}
