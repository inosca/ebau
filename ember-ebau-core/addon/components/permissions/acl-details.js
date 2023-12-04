import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { confirm } from "ember-uikit";

export default class AclDetails extends Component {
  @service notification;
  @service intl;

  @action
  async revokeAcl(acl) {
    try {
      if (await confirm(this.intl.t("permissions.confirmRevoke"))) {
        await acl.revoke();
      }
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("permissions.revokeError"));
    }
  }
}
