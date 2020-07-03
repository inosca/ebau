import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { timeout } from "ember-concurrency";
import { dropTask } from "ember-concurrency-decorators";

import config from "../../../config/environment";

export default class LoadingTextComponent extends Component {
  @tracked dots = ".";

  @dropTask
  *animate() {
    while (config.environment !== "test") {
      yield timeout(500);

      if (this.dots.length >= 3) {
        this.dots = ".";
      } else {
        this.dots += ".";
      }

      this.animate.perform();
    }
  }
}
