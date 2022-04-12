import Route from "@ember/routing/route";
import { next } from "@ember/runloop";
import { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

export default class PublicationIndexRoute extends Route {
  @service router;

  redirect() {
    next(async () => {
      // eslint-disable-next-line ember/no-controller-access-in-routes
      const publications = await this.controllerFor("publication").publications;
      const latest = decodeId(publications?.[publications.length - 1]?.node.id);

      if (latest) {
        this.router.replaceWith("publication.edit", latest);
      }
    });
  }
}
