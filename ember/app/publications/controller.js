import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, restartableTask } from "ember-concurrency-decorators";

export default class IndexController extends Controller {
  @service store;
  @service notification;
  @service router;

  @tracked page = 1;
  @tracked publications = [];

  get hasNextPage() {
    const pagination = this.fetchPublications.lastSuccessful?.value?.meta
      .pagination;

    return pagination && pagination.page < pagination.pages;
  }

  @restartableTask
  *fetchPublications() {
    const publications = yield this.store.query("publication-entry", {
      include: "instance,instance.location",
      page: { number: this.page, size: 20 },
      sort: "instance__location__name",
    });

    this.publications = [...this.publications, ...publications.toArray()];

    return publications;
  }

  @dropTask
  *navigate(publication) {
    yield this.router.transitionTo(
      "instances.edit",
      publication.instance.get("id"),
      {
        queryParams: { publication: publication.id },
      }
    );
  }

  @dropTask
  *fetchMore() {
    this.page++;

    yield this.fetchPublications.perform();
  }
}
