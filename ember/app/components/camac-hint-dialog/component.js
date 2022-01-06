import { getOwner } from "@ember/application";
import Component from "@ember/component";
import { computed } from "@ember/object";

const CamacHintDialogComponent = Component.extend({
  tagName: "span",

  classNames: ["uk-margin-small-left"],

  classNameBindings: ["highlight:uk-text-danger"],

  highlight: false,

  modalId: computed("elementId", function () {
    return `${this.elementId}-hint-modal`;
  }),

  target: computed("modalId", function () {
    return `target: #${this.modalId}`;
  }),

  didInsertElement(...args) {
    this._super(...args);

    this.set(
      "modalContainer",
      getOwner(this)
        .lookup("service:-document")
        .querySelector("#modal-container")
    );
  },
});

CamacHintDialogComponent.reopenClass({
  positionalParams: ["text"],
});

export default CamacHintDialogComponent;
