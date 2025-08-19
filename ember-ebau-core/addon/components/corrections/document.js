import { getOwner } from "@ember/application";
import { service } from "@ember/service";
import { getOwnConfig, macroCondition } from "@embroider/macros";
import Component from "@glimmer/component";
import { parseDocument } from "@projectcaluma/ember-form/lib/parsers";
import { queryManager } from "ember-apollo-client";
import { task } from "ember-concurrency";
import { confirm } from "ember-uikit";
import { trackedFunction } from "reactiveweb/function";

import getActiveDistributionQuery from "ember-ebau-core/gql/queries/get-active-distribution.graphql";
import getDocumentQuery from "ember-ebau-core/gql/queries/get-document.graphql";

export default class CorrectionsDocument extends Component {
  @service fetch;
  @service intl;
  @service router;
  @service notification;
  @service ebauModules;
  @queryManager apollo;

  document = trackedFunction(this, async () => {
    const rawCase = await this.apollo.query(
      {
        query: getDocumentQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.args.instance.id },
      },
      "allCases.edges",
    );
    const form = rawCase[0].node.document.form;
    const answerDocument = rawCase[0].node.document;
    const owner = getOwner(this);
    const Document = owner.factoryFor("caluma-model:document").class;
    const raw = parseDocument({ ...answerDocument, form });

    const document = new Document({ raw, owner });
    return document;
  });

  hasActiveDistribution = trackedFunction(this, async () => {
    const workItems = await this.apollo.query(
      {
        query: getActiveDistributionQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.args.instance.id },
      },
      "allWorkItems",
    );
    return workItems.totalCount > 0;
  });

  get invalidFields() {
    return this.document.value.fields.filter(
      (field) => !field.hidden && field.isInvalid,
    );
  }

  startCorrection = task({ drop: true }, async () => {
    if (!(await confirm(this.intl.t("corrections.document.confirm")))) {
      return;
    }

    try {
      await this.documentCorrection.perform();
      await this.ebauModules.redirectToInstanceForm(this.args.instance.id);

      // need this to have current data on the whole page
      location.reload();
    } catch {
      // error messages are handled in documentCorrection task
    }
  });

  finishCorrection = task({ drop: true }, async (validate) => {
    const valid = await validate();
    if (!valid) {
      return;
    }

    // TODO: Remove this as soon as kt. Bern translations are available
    // Disable confirm finish dialog for kt. Bern
    if (macroCondition(getOwnConfig().application !== "be")) {
      if (
        !(await confirm(this.intl.t("corrections.document.confirm-finish")))
      ) {
        return;
      }
    }

    try {
      await this.documentCorrection.perform();

      // need this to have current data on the whole page
      location.reload();
    } catch {
      // error messages are handled in documentCorrection task
    }
  });

  documentCorrection = task({ drop: true }, async () => {
    try {
      await this.fetch.fetch(
        `/api/v1/instances/${this.args.instance.id}/correction`,
        {
          method: "POST",
        },
      );
    } catch (error) {
      if (error.cause) {
        this.notification.danger(error.cause.map((e) => e.detail).join("<br>"));
      } else {
        this.notification.danger(this.intl.t("corrections.document.error"));
      }

      throw error;
    }
  });
}
