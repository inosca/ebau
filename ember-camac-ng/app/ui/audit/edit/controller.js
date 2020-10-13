import Controller, { inject as controller } from "@ember/controller";

export default class AuditEditController extends Controller {
  @controller("audit") auditController;
  @controller("audit.index") auditIndexController;

  queryParams = ["displayedForm"];

  get audit() {
    return this.auditIndexController.audits.find(
      (audit) => audit.id === this.model
    );
  }

  get disabled() {
    if (!this.audit) {
      return false;
    }

    return this.auditController.disabled || !this.audit.canEdit;
  }
}
