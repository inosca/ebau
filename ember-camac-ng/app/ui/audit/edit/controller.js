import Controller, { inject as controller } from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";

export default class AuditEditController extends Controller {
  @service materialExamSwitcher;

  @controller("audit") auditController;

  queryParams = ["displayedForm"];

  get audit() {
    return [
      ...(this.auditController.audits || []),
      ...(this.auditController.auditsWithSameEbauNumber || []).flatMap(
        (group) => group.audits
      ),
    ].find((audit) => audit.id === this.model);
  }

  get isMaterialExam() {
    return this.audit?.form === "mp-form";
  }

  @dropTask
  *back(event) {
    event.preventDefault();

    yield this.auditController.fetchAudit.perform();
    yield this.transitionToRoute("audit.index");
  }

  @action
  toggleIrrelevant() {
    if (!this.isMaterialExam) return;

    this.materialExamSwitcher.toggle();
  }
}
