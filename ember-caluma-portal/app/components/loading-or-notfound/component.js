import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { restartableTask, timeout } from "ember-concurrency";

import config from "caluma-portal/config/environment";

export default class LoadingOrNotfoundComponent extends Component {
  @tracked state = "loading";

  @restartableTask
  *setTemplate() {
    // debounce setting of the template name for 50ms to avoid rapid changing of
    // the rendered content, e.g. a short flickering of a 404 error between the
    // loading state and the actual content
    if (config.environment !== "test") {
      yield timeout(50);
    }

    this.state = this.args.loading
      ? "loading"
      : !this.args.hasPermission
      ? "no-permission"
      : null;
  }
}
