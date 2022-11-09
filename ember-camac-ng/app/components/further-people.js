import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

import redirectConfig from "camac-ng/config/redirect";

export default class FurtherPeopleComponent extends Component {
  @service shoebox;

  get formInstanceResourceId() {
    return redirectConfig.instanceResourceRedirects.form[
      this.shoebox.content.roleId
    ];
  }
}
