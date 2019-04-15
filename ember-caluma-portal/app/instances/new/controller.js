import Controller from "@ember/controller";
import { task } from "ember-concurrency";
import { info1, info2 } from "ember-caluma-portal/instances/new/info";
import { inject as service } from "@ember/service";
import mutation from "ember-caluma-portal/gql/mutations/start-case";

export default Controller.extend({
  apollo: service(),

  infoCol1: info1,
  infoCol2: info2,

  selectedForm: null,

  save: task(function*() {
    const caseId = yield this.get("apollo").mutate(
      {
        mutation,
        variables: {
          input: {
            workflow: "building-permit",
            form: this.selectedForm
          }
        }
      },
      "startCase.case.id"
    );

    yield this.transitionToRoute("instances.edit", caseId);
  }).drop()
});
