import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask, lastValue } from "ember-concurrency";

export default class TextcomponentComponent extends Component {
  @service store;
  @service shoebox;

  @lastValue("getTextcomponents") textcomponents;
  @dropTask
  *getTextcomponents() {
    let textcomponents = this.store
      .peekAll("notification-template")
      .filter((template) => {
        return (
          parseInt(template.belongsTo("service").id()) ===
            this.shoebox.content.serviceId && template.type === "textcomponent"
        );
      });

    if (!textcomponents.length) {
      textcomponents = yield this.store.query("notification-template", {
        service: this.shoebox.content.serviceId,
        type: "textcomponent",
      });
    }

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
  applyTextcomponent(textcomponent, e) {
    e.preventDefault();

    this.args.field.answer.value = [
      this.args.field.answer.value,
      textcomponent.body,
    ].join("");
  }
}
