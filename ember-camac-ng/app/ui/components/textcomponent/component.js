import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class TextcomponentComponent extends Component {
  @service store;
  @service shoebox;

  @lastValue("getTextcomponents") textcomponents;
  @dropTask
  *getTextcomponents() {
    const textcomponents = yield this.store.query("notification-template", {
      service: this.shoebox.content.serviceId,
      type: "textcomponent",
    });

    const sortedTextcomponents = {};

    textcomponents.forEach((textcomponent) => {
      if (!(textcomponent.purpose in sortedTextcomponents)) {
        sortedTextcomponents[textcomponent.purpose] = [];
      }

      sortedTextcomponents[textcomponent.purpose].push(textcomponent);
    });

    return sortedTextcomponents;
  }

  @action
  applyTextcomponent(textcomponent) {
    this.args.field.answer.value = [
      this.args.field.answer.value,
      textcomponent.body,
    ].join("");
  }
}
