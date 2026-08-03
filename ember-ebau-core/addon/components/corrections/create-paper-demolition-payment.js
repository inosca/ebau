import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";

export default class CorrectionsCreatePaperDemolitionPayment extends Component {
  @service fetch;
  @service intl;
  @service notification;
  @service ebauModules;

  createDossier = task({ drop: true }, async (event) => {
    event.preventDefault();

    try {
      const response = await this.fetch.fetch(`/api/v1/instances`, {
        method: "POST",
        body: JSON.stringify({
          data: {
            attributes: {
              "caluma-form": "auszahlung-abbruchpraemie",
              "copy-source": this.args.instance.id,
              "copy-type": "demolition_payment",
            },
            type: "instances",
          },
        }),
      });
      const { data } = await response.json();
      this.ebauModules.redirectToInstance(data.id);
    } catch {
      this.notification.danger(
        this.intl.t("corrections.create-paper-demolition-payment.error"),
      );
    }
  });
}
