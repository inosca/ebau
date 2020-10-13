import { getOwner, setOwner } from "@ember/application";
import { A } from "@ember/array";
import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { decodeId } from "ember-caluma/helpers/decode-id";
import { dropTask } from "ember-concurrency-decorators";

import { confirmTask } from "camac-ng/decorators";
import completeWorkItem from "camac-ng/gql/mutations/complete-work-item";
import createAuditDocument from "camac-ng/gql/mutations/create-audit-document";
import deleteDocument from "camac-ng/gql/mutations/delete-document";
import linkAuditDocument from "camac-ng/gql/mutations/link-audit-document";
import skipWorkItem from "camac-ng/gql/mutations/skip-work-item";

class Audit {
  @service store;
  @service shoebox;

  constructor(raw) {
    this._raw = raw;
  }

  get id() {
    return decodeId(this._raw.id);
  }

  get type() {
    return this._raw.form.name;
  }

  get createdBy() {
    return this.store.peekRecord("service", this._raw.createdByGroup);
  }

  get createdAt() {
    return this._raw.createdAt;
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

  @queryManager apollo;

  @controller("audit") auditController;

  get disabled() {
    return this.auditController.disabled;
  }

  get forms() {
    return ["fp-form", "mp-form", "bab-form"];
  }

  get audits() {
    return A(
      this.auditController.auditWorkItem?.document.answers.edges.flatMap(
        (edge) =>
          edge.node.value.map((raw) => {
            const audit = new Audit(raw);

            setOwner(audit, getOwner(this));

            return audit;
          })
      )
    )
      .sortBy("type", "createdAt")
      .reverse();
  }

  getTableAnswerValue(audit, form) {
    const tableAnswer = audit.answers.edges
      .map((edge) => edge.node)
      .find((node) => node.question.rowForm.slug === form);

    if (!tableAnswer) {
      return [];
    }

    return tableAnswer.value.map((doc) => decodeId(doc.id));
  }

  @dropTask
  *createAudit(form, event) {
    event.preventDefault();

    try {
      // create empty document
      const documentId = yield this.apollo.mutate(
        {
          mutation: createAuditDocument,
          variables: { form },
        },
        "saveDocument.document.id"
      );

      const value = new Set(
        this.getTableAnswerValue(
          this.auditController.auditWorkItem.document,
          form
        )
      );

      value.add(decodeId(documentId));

      // link document to the right table
      yield this.apollo.mutate({
        mutation: linkAuditDocument,
        variables: {
          question: form,
          document: decodeId(this.auditController.auditWorkItem.document.id),
          value: [...value],
        },
      });

      yield this.auditController.fetchAudit.perform();

      yield this.transitionToRoute("audit.edit", decodeId(documentId));
    } catch (error) {
      this.notifications.error(this.intl.t("audit.createError"));
    }
  }

  @dropTask
  @confirmTask("audit.deleteConfirm")
  *deleteAudit(audit) {
    try {
      const value = new Set(
        this.getTableAnswerValue(
          this.auditController.auditWorkItem.document,
          audit.form
        )
      );

      value.delete(audit.id);

      // unlink audit
      yield this.apollo.mutate({
        mutation: linkAuditDocument,
        variables: {
          question: audit.form,
          document: decodeId(this.auditController.auditWorkItem.document.id),
          value: [...value],
        },
      });

      // delete document
      yield this.apollo.mutate({
        mutation: deleteDocument,
        variables: { id: audit.id },
      });

      yield this.auditController.fetchAudit.perform();

      this.notifications.success(this.intl.t("audit.deleteSuccess"));
    } catch (error) {
      this.notifications.error(this.intl.t("audit.deleteError"));
    }
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
}
