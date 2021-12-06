import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { timeout } from "ember-concurrency";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import dateTime from "camac-ng/utils/date-time";

export default class DossierImportDetailController extends Controller {
  @service intl;
  @service notifications;
  @service store;
  @service shoebox;
  @service session;
  @service router;
  @service fetch;

  @tracked user;

  @lastValue("fetchImport") import;
  @dropTask
  *fetchImport() {
    this.notifications.clear();

    const response = yield this.fetch.fetch(
      `/api/v1/dossier-imports/${this.model}?${new URLSearchParams({
        include: "user",
      })}`,
      {
        method: "GET",
      }
    );

    if (!response.ok) {
      this.notifications.error(
        this.intl.t("dossierImport.detail.fetchImportError")
      );
      this.router.transitionTo("index");
      return;
    }
    const data = yield response.json();
    const attrs = data.included[0].attributes;
    this.user = `${attrs.name} ${attrs.surname}`;
    return data.data.attributes;
  }

  @dropTask
  *deleteImport() {
    this.notifications.clear();

    const response = yield this.fetch.fetch(
      `/api/v1/dossier-imports/${this.model}`,
      {
        method: "DELETE",
      }
    );

    if (!response.ok) {
      this.notifications.error(
        this.intl.t("dossierImport.detail.actions.deleteImport.error")
      );
    } else if (response.ok) {
      this.notifications.success(
        this.intl.t("dossierImport.detail.actions.deleteImport.success")
      );
      this.router.transitionTo("dossier-import.index");
    }
  }

  @dropTask
  *startImport() {
    // TODO as soon as workflow is implemented in backend
    yield timeout(1000);
  }

  get creationDate() {
    const creationDate = new Date(this.import?.["created-at"]);
    return creationDate ? dateTime(creationDate) : null;
  }

  get summary() {
    const messages = this.import?.messages;
    return this.isValidated
      ? messages?.validation.summary
      : this.isImported
      ? messages?.import.summary
      : null;
  }

  get isValidated() {
    return (
      this.import?.status === "verified" || this.import?.status === "failed"
    );
  }

  get isImported() {
    return this.import?.status === "done";
  }

  get validationVerified() {
    return this.import?.status === "verified";
  }

  get validationFailed() {
    return this.import?.status === "failed";
  }
}
