import { getOwner } from "@ember/application";
import Service from "@ember/service";
import { findRecord } from "ember-data-resources";
import config from "ember-ebau-core/config/main";

export default class ShoeboxService extends Service {
  get content() {
    const shoebox = getOwner(this)
      .lookup("service:-document")
      .querySelector("#ember-camac-ng-shoebox");

    try {
      return JSON.parse(shoebox.innerHTML);
    } catch {
      return {};
    }
  }

  get serviceGroupId() {
    return this.content.serviceGroupId;
  }

  get role() {
    const roleId = this.content.roleId;
    const roles = this.content.config?.roles;

    if (!roleId || !roles) return null;

    const role = Object.entries(roles).find(([, ids]) =>
      ids.map((id) => parseInt(id)).includes(roleId),
    );

    return role && role[0];
  }

  get baseRole() {
    return this.role
      ?.replace(/-admin$/, "")
      .replace(/-lead$/, "")
      .replace(/-clerk$/, "")
      .replace(/-readonly$/, "")
      .replace(/^sub/, "");
  }

  get isReadOnlyRole() {
    return (
      this.role?.endsWith("-readonly") || // BE
      this.role === "readonly" // SZ
    );
  }

  get isAdminRole() {
    return this.role?.endsWith("-admin");
  }

  get isLeadRole() {
    return this.role?.endsWith("-lead") || this.role === "subservice";
  }

  get isSupportRole() {
    return this.role === "support";
  }

  get isMunicipalityLeadRole() {
    return this.role === "municipality-lead";
  }

  get isCoordinationRole() {
    return ["coordination", "coordination-lead"].includes(this.role);
  }

  get isTrustedServiceRole() {
    return this.content.roleId === config.trustedServiceRole;
  }

  service = findRecord(this, "service", () => [
    this.shoebox.serviceId,
    { include: "service_group" },
  ]);

  get serviceSlug() {
    return this.service.record?.slug;
  }

  get serviceGroupSlug() {
    return this.service.record?.serviceGroup.get("slug");
  }
}
