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
  *navigate(publication) {
    yield this.transitionToRoute(
      "instances.edit",
      publication.instance.get("id"),
      {
        queryParams: { publication: publication.id },
      }
    );
  }
}
