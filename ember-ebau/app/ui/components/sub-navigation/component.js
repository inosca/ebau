import Component from "@glimmer/component";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

export default class SubNavigationComponent extends Component {
  @service store;

  instanceResources = trackedTask(this, this.fetchInstanceResources, () => [
    this.args.instanceId,
  ]);

  @dropTask
  *fetchInstanceResources() {
    yield Promise.resolve();

    const irs = yield this.store.query("instance-resource", {});

    return irs;
  }
}
