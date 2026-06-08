import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import documentValidityQuery from "@projectcaluma/ember-form/gql/queries/document-validity.graphql";
import { queryManager } from "ember-apollo-client";
import { task } from "ember-concurrency";
import { confirm } from "ember-uikit";
import { trackedFunction } from "reactiveweb/function";
import { localCopy } from "tracked-toolbox";

import getCaseMetaQuery from "ember-ebau-core/gql/queries/get-case-meta.graphql";

export default class CorrectionsChangeForm extends Component {
  @service fetch;
  @service intl;
  @service notification;
  @service ebauModules;
  @queryManager apollo;

  @localCopy("args.instance.calumaForm") form;

  documentId = trackedFunction(this, async () => {
    return await this.apollo.query(
      {
        query: getCaseMetaQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.args.instance.id },
      },
      "allCases.edges.0.node.document.id",
    );
  });

  availableForms = trackedFunction(this, async () => {
    const response = await this.fetch.fetch(
      `/api/v1/instances/${this.args.instance.id}/changeable-forms`,
    );
    const { data } = await response.json();

    return data;
  });

  @action
  setForm(event) {
    this.form = event.target.value;
  }

  isValid = trackedFunction(this, async () => {
    const documentId = this.documentId.value;
    if (!documentId) {
      return null;
    }

    return await this.apollo.query(
      {
        query: documentValidityQuery,
        fetchPolicy: "network-only",
        variables: { id: documentId },
      },
      "documentValidity.edges.0.node.isValid",
    );
  });

  get showHint() {
    return !this.isValid.isLoading && this.isValid.value === false;
  }

  save = task({ drop: true }, async (event) => {
    event.preventDefault();

    if (!(await confirm(this.intl.t("corrections.change-form.confirm")))) {
      return;
    }

    try {
      await this.fetch.fetch(
        `/api/v1/instances/${this.args.instance.id}/change-form`,
        {
          method: "POST",
          body: JSON.stringify({
            data: {
              type: "instance-change-forms",
              id: this.args.instance.id,
              attributes: { form: this.form },
            },
          }),
        },
      );

      if (this.ebauModules.isLegacyApp) {
        // sadly we need this to have current data on the whole page
        location.reload();
      } else {
        await this.args.instance.reload();

        // reload document validity after changing the form, to show the hint
        // if the form is invalid.
        await this.isValid.retry();

        this.notification.success(
          this.intl.t("corrections.change-form.success"),
        );
      }
    } catch {
      this.notification.danger(this.intl.t("corrections.change-form.error"));
    }
  });
}
