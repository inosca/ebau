import Controller from "@ember/controller";
import { action, computed } from "@ember/object";
import { isBlank } from "@ember/utils";
import { tracked } from "@glimmer/tracking";
import Changeset from "ember-changeset";
import { dropTask, restartableTask } from "ember-concurrency-decorators";
import UIkit from "uikit";

export default class InstancesEditInvolviertePersonenController extends Controller {
  @tracked applicants = null;
  @tracked saveErrors = [];
  @tracked newRow;

  @dropTask
  *addRow() {
    yield this.set("newRow", { email: undefined });
  }

  @restartableTask
  *saveRow() {
    const changeset = this._value;

    yield changeset.validate();

    if (changeset.get("isValid")) {
      changeset.execute();

      const applicant = this.store.createRecord("applicant", {
        email: this.newRow.email,
        instance: this.model.instance
      });

      try {
        yield applicant.save();
      } catch (exception) {
        this.saveErrors = exception.errors.map(e => e.detail);
        return;
      }

      yield this.refreshList();

      this.set("newRow", null);
      UIkit.modal("#modal-applicants").hide();
    }
  }

  @dropTask
  *deleteRow(row) {
    yield this.applicants.find(a => a.email === row.email).destroyRecord();
    yield this.refreshList();
  }

  async refreshList() {
    this.set(
      "applicants",
      await this.store
        .peekAll("applicant")
        .filterBy("id")
        .filterBy("instance.id", this.get("model.instance.id"))
    );
  }

  @computed("newRow")
  get _value() {
    return new Changeset(
      this.newRow || {},
      (...args) => this._validate(...args),
      { email: () => this._validate }
    );
  }

  _validate({ newValue }) {
    try {
      const validations = [
        value =>
          !isBlank(value) || "Dieses Feld darf nicht leer gelassen werden",
        value =>
          !this.applicants.filterBy("email", value).length ||
          "Die Person mit dieser E-Mailadresse wurde schon eingeladen"
      ];

      const isValid = validations.map(fn => fn(newValue));

      return (
        isValid.every(v => v === true) ||
        isValid.filter(v => typeof v === "string")
      );
    } catch (e) {
      return false;
    }
  }

  @action
  change(name, { target: { value } }) {
    this.set(`newRow.${name}`, value);
  }
}
