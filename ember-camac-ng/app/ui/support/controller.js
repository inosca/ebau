import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import config from "camac-ng/config/environment";
import { confirmTask } from "camac-ng/decorators";
import getFormsQuery from "camac-ng/gql/queries/get-forms";
import parseErrors from "camac-ng/utils/parse-errors";

export default class SupportController extends Controller {
  @queryManager apollo;

  @service store;
  @service fetch;
  @service intl;
  @service notifications;

  @tracked ebauNumber;
  @tracked _form;

  get form() {
    return this.forms.find((form) => form.value === this._form);
  }

  set form(event) {
    this._form = event.target.value;
  }

  @dropTask
  *setup() {
    yield this.fetchInstance.perform();
    yield this.fetchForms.perform();
  }

  @lastValue("fetchInstance") instance = null;
  @dropTask
  *fetchInstance() {
    const instance = yield this.store.findRecord("instance", this.model);

    yield instance.fetchEbauNumber.perform();

    this.ebauNumber = instance.ebauNumber || "";
    this._form = instance.calumaForm;

    return instance;
  }

  @lastValue("fetchForms") forms = [];
  @dropTask
  *fetchForms() {
    const forms = yield this.apollo.query(
      {
        query: getFormsQuery,
        variables: { forms: config.APPLICATION.interchangeableForms },
      },
      "allForms.edges"
    );

    return forms.map(({ node }) => ({ value: node.slug, label: node.name }));
  }

  @dropTask
  @confirmTask("support.archive.confirm")
  *archive() {
    try {
      yield this.fetch.fetch(`/api/v1/instances/${this.model}/archive`, {
        method: "POST",
      });

      // sadly we need this to have current data on the whole page
      location.reload();
    } catch (error) {
      this.notifications.error(this.intl.t("support.archive.error"));
    }
  }

  @dropTask
  @confirmTask("support.ebau-number.confirm")
  *changeEbauNumber() {
    try {
      yield this.fetch.fetch(
        `/api/v1/instances/${this.model}/set-ebau-number`,
        {
          method: "POST",
          body: JSON.stringify({
            data: {
              type: "instance-set-ebau-numbers",
              id: this.model,
              attributes: {
                "ebau-number": this.ebauNumber,
              },
            },
          }),
        }
      );

      // sadly we need this to have current data on the whole page
      location.reload();
    } catch (error) {
      let text = this.intl.t("support.ebau-number.error");

      if (error.response) {
        const { errors } = yield error.response.json();

        if (errors) {
          text = parseErrors(errors);
        }
      }

      this.notifications.error(text);
    }
  }

  @dropTask
  @confirmTask("support.change-form.confirm")
  *changeForm() {
    try {
      yield this.fetch.fetch(`/api/v1/instances/${this.model}/change-form`, {
        method: "POST",
        body: JSON.stringify({
          data: {
            type: "instance-change-forms",
            id: this.model,
            attributes: {
              form: this.form.value,
            },
          },
        }),
      });

      // sadly we need this to have current data on the whole page
      location.reload();
    } catch (error) {
      this.notifications.error(this.intl.t("support.change-form.error"));
    }
  }
}
