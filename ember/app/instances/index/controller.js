import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { task, timeout } from "ember-concurrency";
import QueryParams from "ember-parachute";

export const queryParams = new QueryParams({
  group: {
    defaultValue: null,
    refresh: true,
    replace: true
  },
  sort: {
    defaultValue: "-creation_date",
    refresh: true,
    replace: true
  },
  sort_form_field: {
    defaultValue: "",
    refresh: true,
    replace: true
  },
  identifier: {
    defaultValue: "",
    refresh: true,
    replace: true
  }
});

export default Controller.extend(queryParams.Mixin, {
  notification: service(),

  setup() {
    this.data.perform();
  },

  queryParamsDidChange({ shouldRefresh, changed }) {
    if (shouldRefresh) {
      this.data.perform();
    }

    if (changed.sort) {
      this.resetQueryParams(["sort_form_field"]);
    }
  },

  reset(_, isExiting) {
    if (isExiting) {
      this.resetQueryParams();
    }
  },

  data: task(function*() {
    const instances = yield this.store.query("instance", {
      ...this.allQueryParams,
      include: "form,instance-state,location",
      is_applicant: 1
    });
    yield this.store.query("form-field", {
      instance: instances.mapBy("id").join(","),
      name: "bezeichnung,projektnummer,bauherrschaft"
    });
    return instances;
  }).restartable(),

  search: task(function*(event) {
    yield timeout(500);

    this.set("identifier", event.target.value);
  }).restartable(),

  delete: task(function*(instance) {
    try {
      yield instance.destroyRecord();
    } catch (e) {
      this.notification.danger("Das Gesuch konnte nicht gelöscht werden");
    }
  }).drop()
});
