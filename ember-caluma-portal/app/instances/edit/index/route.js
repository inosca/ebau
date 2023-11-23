import Route from "@ember/routing/route";
import { next } from "@ember/runloop";
import { inject as service } from "@ember/service";

import { isEmbedded } from "caluma-portal/helpers/is-embedded";

export default class InstancesEditIndexRoute extends Route {
  @service router;
  @service store;

  redirect() {
    next(async () => {
      // redirect directly to the main form if the app is embedded
      if (isEmbedded()) {
        const instance = await this.store.findRecord(
          "instance",
          this.modelFor("instances.edit"),
        );

        this.router.replaceWith("instances.edit.form", instance.calumaForm);
      }
    });
  }
}
