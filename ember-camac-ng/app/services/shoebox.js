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
    const roles = this.content.config?.roles;

    if (!roleId || !roles) return null;

    const role = Object.entries(roles).find(([, ids]) =>
      ids.map((id) => parseInt(id)).includes(roleId)
    );

    return role && role[0];
  }

  get isReadOnlyRole() {
    return this.role?.endsWith("-readonly");
  }

  get isAdminRole() {
    return this.role?.endsWith("-admin");
  }

  get isSupportRole() {
    return this.role === "support";
  }

  get isMunicipalityLeadRole() {
    return this.role === "municipality-lead";
  }
}
