import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";
import { computed } from "@ember/object";
import Changeset from "ember-changeset";
import { isBlank } from "@ember/utils";
import UIkit from "uikit";

export default Controller.extend({
  ajax: service(),

  init() {
    this._super(...arguments);
  },

  addRow: task(function*() {
    yield this.set("newRow", { email: undefined });
  }).drop(),

  saveRow: task(function*() {
    let changeset = this._value;

    yield changeset.validate();

    if (changeset.get("isValid")) {
      changeset.execute();

      let applicant = this.store.createRecord("applicant", {
        email: this.get("newRow.email"),
        instance: this.get("model.instance")
      });

      try {
        yield applicant.save();
      } catch (exception) {
        this.set("saveErrors", exception.errors.map(e => e.detail));
        return;
      }

      yield this.refreshList();

      this.set("newRow", null);
      UIkit.modal("#modal-applicants").hide();
    }
  }).restartable(),

  deleteRow: task(function*(row) {
    yield this.applicants.find(a => a.email === row.email).destroyRecord();
    yield this.refreshList();
  }),

  async refreshList() {
    this.set(
      "applicants",
      await this.store
        .peekAll("applicant")
        .filterBy("id")
        .filterBy("instance.id", this.get("model.instance.id"))
    );
  },

  _value: computed("newRow", function() {
    return new Changeset(
      this.newRow || {},
      (...args) => this._validate(...args),
      { email: () => this._validate }
    );
  }),

  _validate({ newValue }) {
    try {
      let validations = [
        value =>
          !isBlank(value) || "Dieses Feld darf nicht leer gelassen werden",
        value =>
          !this.applicants.filterBy("email", value).length ||
          "Diese E-Mail wurde schon eingeladen"
      ];

      let isValid = validations.map(fn => fn(newValue));

      return (
        isValid.every(v => v === true) ||
        isValid.filter(v => typeof v === "string")
      );
    } catch (e) {
      return false;
    }
  },

  actions: {
    change(name, value) {
      this.set(`_value.${name}`, value);
    }
  }
});
