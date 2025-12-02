import { service } from "@ember/service";
import Component from "@glimmer/component";

export default class BeInfoTableErrorsComponent extends Component {
  @service intl;

  get tables() {
    const document = this.args.field.document;
    return [
      document.findField("sollzustand-tabelle-v5"),
      document.findField("aufnahme-istzustand-tabelle-v5"),
    ].filter(Boolean);
  }

  get hasRowErrors() {
    const targetMessage = this.intl.t("caluma.form.validation.table");

    return this.tables.some((table) => {
      return table.errors.some((error) => error === targetMessage);
    });
  }
}
