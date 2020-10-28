import { getOwner } from "@ember/application";
import Service from "@ember/service";

export default class ShoeboxService extends Service {
  get content() {
    const shoebox = getOwner(this)
      .lookup("service:-document")
      .querySelector("#ember-camac-ng-shoebox");

    try {
      return JSON.parse(shoebox.innerHTML);
    } catch (error) {
      return {};
    }
  }

  get role() {
    const roleId = this.content.roleId;
    const config = this.content.config.roles;

    if (!roleId) return null;

    const role = Object.entries(config).find(([, ids]) =>
      ids.map((id) => parseInt(id)).includes(roleId)
    );

    return role && role[0];
  }
}
