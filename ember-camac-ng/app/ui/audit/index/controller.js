import { getOwner, setOwner } from "@ember/application";
import { A } from "@ember/array";
import Controller, { inject as controller } from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { decodeId } from "ember-caluma/helpers/decode-id";
import { dropTask } from "ember-concurrency-decorators";

import { confirmTask } from "camac-ng/decorators";
import completeWorkItem from "camac-ng/gql/mutations/complete-work-item";
import skipWorkItem from "camac-ng/gql/mutations/skip-work-item";

class Audit {
  @service store;
  @service shoebox;

  constructor(raw, caseData) {
    this._raw = raw;
    this._caseData = caseData;
  }

  get instanceId() {
    return this._caseData.instanceId;
  }

  get id() {
    return decodeId(this._raw.id);
  }

  get type() {
    return this._raw.form.name;
  }

  get municipality() {
    return this.store.peekRecord("service", this._raw.createdByGroup);
  }

  get modifiedByUser() {
    return (
      this._raw.modifiedContentByUser &&
      this.store
        .peekAll("public-user")
        .find((user) => user.username === this._raw.modifiedContentByUser)
    );
  }

  get modifiedByService() {
    return (
      this._raw.modifiedContentByGroup &&
      this.store.peekRecord("service", this._raw.modifiedContentByGroup)
    );
  }

  get modifiedAt() {
    return this._raw.modifiedContentAt;
  }

  get form() {
    return this._raw.form.slug;
  }

  get canEdit() {
    return (
      parseInt(this._raw.createdByGroup) ===
      parseInt(this.shoebox.content.serviceId)
    );
  }
}

export default class AuditIndexController extends Controller {
  @service notifications;
  @service intl;
  @service fetch;

  @queryManager apollo;

  @controller("audit") auditController;

  @tracked showSameEbauNumber = false;

  get disabled() {
    return this.auditController.disabled;
  }

  get audits() {
    return A(
      this.auditController.auditWorkItem?.document.answers.edges.flatMap(
        (edge) =>
          edge.node.value.map((raw) =>
            this.createAudit(raw, this.auditController.auditWorkItem.caseData)
          )
      )
    )
      .sortBy("type", "createdAt")
      .reverse();
  }

  get auditsWithSameEbauNumber() {
    const workItems = this.auditController.audits?.filter(
      (workItem) => workItem.caseData.instanceId !== this.model
    );

    return workItems
      ?.map((workItem) => {
        return {
          instanceId: workItem.caseData.instanceId,
          form: workItem.caseData.form,
          audits: workItem.document.answers.edges.flatMap((edge) =>
            edge.node.value.map((raw) =>
              this.createAudit(raw, workItem.caseData)
            )
          ),
        };
      })
      .filter((auditGroup) => auditGroup.audits.length);
  }

  get documentData() {
    const document = this.auditController.auditWorkItem?.document;

    return (
      document && {
        id: decodeId(document.id),
        ...document.answers.edges.reduce((obj, { node }) => {
          return {
            ...obj,
            [node.question.rowForm.slug]: node.value.map((doc) =>
              decodeId(doc.id)
            ),
          };
        }, {}),
      }
    );
  }

  createAudit(rawDocument, caseData) {
    const audit = new Audit(rawDocument, caseData);

    setOwner(audit, getOwner(this));

    return audit;
  }

  @dropTask
  @confirmTask("audit.skipConfirm")
  *skipAudit() {
    try {
      yield this.apollo.mutate({
        mutation: skipWorkItem,
        variables: { id: this.auditController.auditWorkItem.id },
      });

      yield this.auditController.fetchAudit.perform();

      this.notifications.success(this.intl.t("audit.skipSuccess"));
    } catch (error) {
      this.notifications.error(this.intl.t("audit.skipError"));
    }
  }

  @dropTask
  @confirmTask("audit.completeConfirm")
  *completeAudit() {
    try {
      yield this.apollo.mutate({
        mutation: completeWorkItem,
        variables: { id: this.auditController.auditWorkItem.id },
      });

      yield this.auditController.fetchAudit.perform();

      this.notifications.success(this.intl.t("audit.completeSuccess"));
    } catch (error) {
      if (error.errors) {
        // validation failed
        this.notifications.error(this.intl.t("audit.completeInvalid"));
      } else {
        // generic error
        this.notifications.error(this.intl.t("audit.completeError"));
      }
    }
  }

  @action
  toggleShowSameEbauNumber() {
    this.showSameEbauNumber = !this.showSameEbauNumber;
  }
}
