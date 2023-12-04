import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class ErrorComponent extends Component {
  @service intl;

  get errorString() {
    // TODO: decouple from ember-gwr or cleanup when gwr translations got fixed
    return this.args.errors
      ?.map((error) =>
        this.intl.t(`ember-gwr.validation-errors.${error.type}`, error.context),
      )
      .join(", ");
  }
}
