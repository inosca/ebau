import Controller from "@ember/controller";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";

export default Controller.extend({
  store: service(),
  notification: service(),

  publicationList: computed(
    "publications.lastSuccessful.value.[]",
    "publicationPermissions.lastSuccessful.value.[]",
    function() {
      return this.get("publications.lastSuccessful.value").map(publication => {
        this.getWithDefault(
          "publicationPermissions.lastSuccessful.value",
          []
        ).forEach(permission => {
          if (permission.get("publicationEntry.id") === publication.id) {
            publication.set("status", permission.status);
          }
        });

        return publication;
      });
    }
  ),

  publications: task(function*() {
    return yield this.store.query("publication-entry", {
      include: "instance,instance.location"
    });
  }).restartable(),

  publicationPermissions: task(function*() {
    return yield this.store.findAll("publication-entry-user-permission");
  }).restartable(),

  requestPermission: task(function*(publication) {
    const permission = this.store.createRecord(
      "publication-entry-user-permission",
      { status: "pending", publicationEntry: publication }
    );
    try {
      yield permission.save();
    } catch (e) {
      this.notification.danger("Ein Fehler ist aufgetreten");
    }
  }),

  navigate: task(function*(instance) {
    yield this.transitionToRoute("instances.edit", instance.get("id"));
  })
});
