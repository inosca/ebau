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
    this.columns = [
      { label: "E-Mail", name: "email", required: true, type: "email" }
    ];
  },

  addRow: task(function*() {
    let row = {
      ...this.columns.reduce(
        (obj, { name }) => ({ ...obj, [name]: undefined }),
        {}
      )
    };

    yield this.setProperties({
      editedRow: row,
      showEdit: true
    });
  }).drop(),

  saveRow: task(function*() {
    let changeset = this._value;

    yield changeset.validate();

    if (changeset.get("isValid")) {
      changeset.execute();

      let applicant = this.store.createRecord("applicant", {
        email: this.get("editedRow.email"),
        instance: this.get("model.instance")
      });
      this.set("newApplicant", applicant);

      yield applicant.save();

      yield this.refreshList();

      this.setProperties({
        editedRow: null,
        showEdit: false,
        newApplicant: null
      });
      UIkit.modal("#modal-applicants").hide();
    }
  }).restartable(),

  deleteRow: task(function*(row) {
    yield this.applicants.find(a => a.email === row.email).destroyRecord();
    yield this.refreshList();

    this.setProperties({
      editedRow: null,
      showEdit: false
    });
  }),

  async refreshList() {
    this.set(
      "applicants",
      await this.store
        .peekAll("applicant")
        .filterBy("instance.id", this.get("model.instance.id"))
    );
  },

  saveErrors: computed("newApplicant.adapterError.errors.[]", function() {
    return this.getWithDefault("newApplicant.adapterError.errors", []).map(
      e => e.detail
    );
  }),

  _value: computed("editedRow", "columns.[]", function() {
    return new Changeset(
      this.editedRow || {},
      (...args) => this._validate(...args),
      this.columns.reduce((map, f) => {
        return { ...map, [f.name]: () => this._validate };
      }, {})
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
      return true;
    }
  },

  actions: {
    change(name, value) {
      this.set(`_value.${name}`, value);
    }
  }
});
