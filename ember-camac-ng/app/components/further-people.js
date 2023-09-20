import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import mainConfig from "ember-ebau-core/config/main";

export default class FurtherPeopleComponent extends Component {
  @service shoebox;

  get formInstanceResourceId() {
    return mainConfig.instanceResourceRedirects.form[
      this.shoebox.content.roleId
    ];
  }
}
