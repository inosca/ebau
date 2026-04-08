import { service } from "@ember/service";
import Component from "@glimmer/component";

export default class ValidatedFormCustomErrorComponent extends Component {
  @service intl;

  get errorString() {
    return this.args.errors
      ?.map((error) =>
        typeof error === "string"
          ? error
          : this.intl.t(`validation-errors.${error.type}`, error.context),
      )
      .join(", ");
  }
}
