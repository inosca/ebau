import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

export default class RelatedPublicationsComponent extends Component {
  @service store;

  relatedPublicInstances = trackedTask(
    this,
    this.fetchRelatedPublicInstances,
    () => [this.args.dossierNr, this.args.instanceId],
  );

  @dropTask
  *fetchRelatedPublicInstances(dossierNr, instanceId) {
    yield Promise.resolve();

    try {
      return yield this.store.query("public-caluma-instance", {
        dossier_nr: dossierNr,
        exclude_instance: instanceId,
      });
    } catch (e) {
      return [];
    }
  }
}
