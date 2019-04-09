import Component from "@ember/component";
import { computed } from "@ember/object";
import { getOwner } from "@ember/application";

const CamacHintDialogComponent = Component.extend({
  tagName: "span",

  classNames: ["uk-margin-small-left"],

  modalId: computed("elementId", function() {
    return `${this.elementId}-hint-modal`;
  }),

  target: computed("modalId", function() {
    return `target: #${this.modalId}`;
  }),

  didInsertElement() {
    this._super(...arguments);

    this.set(
      "modalContainer",
      getOwner(this)
        .lookup("service:-document")
        .querySelector("#modal-container")
    );
  }
});

CamacHintDialogComponent.reopenClass({
  positionalParams: ["text"]
});

export default CamacHintDialogComponent;
