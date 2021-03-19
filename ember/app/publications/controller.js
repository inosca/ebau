import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask, restartableTask } from "ember-concurrency-decorators";

export default class IndexController extends Controller {
  @service store;
  @service notification;

  @restartableTask
  *publications() {
    return yield this.store.query("publication-entry", {
      include: "instance,instance.location",
    });
  }

  @dropTask
  *navigate(instance) {
    // TODO count amount of clicks
    yield this.transitionToRoute("instances.edit", instance.get("id"), { queryParams: { publication: 1 }});
  }
}
