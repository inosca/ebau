import { getOwner } from "@ember/application";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { parseDocument } from "@projectcaluma/ember-form/lib/parsers";
import { queryManager } from "ember-apollo-client";
import { task } from "ember-concurrency";
import { confirm } from "ember-uikit";
import { trackedFunction } from "reactiveweb/function";

import getDocumentQuery from "ebau/gql/queries/get-document.graphql";

export default class DocumentCorrection extends Component {
  @service fetch;
  @service intl;
  @service router;
  @service notification;
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

  get invalidFields() {
    return this.document.value.fields.filter(
      (field) => !field.hidden && field.isInvalid,
    );
  }

  startCorrection = task({ drop: true }, async () => {
    if (!(await confirm(this.intl.t("corrections.document.confirm")))) {
      return;
    }

    await this.documentCorrection.perform();

    await this.router.transitionTo("cases.detail.form", this.args.instance.id);

    // need this to have current data on the whole page
    location.reload();
  });

  finishCorrection = task({ drop: true }, async (validate) => {
    const valid = await validate();
    if (
      !valid ||
      !(await confirm(this.intl.t("corrections.document.confirm-finish")))
    ) {
      return;
    }

    await this.documentCorrection.perform();

    // need this to have current data on the whole page
    location.reload();
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
    }
  });
}
