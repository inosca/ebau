import Route from "@ember/routing/route";
import { next } from "@ember/runloop";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

export default class PublicationIndexRoute extends Route {
  redirect() {
    next(async () => {
      // eslint-disable-next-line ember/no-controller-access-in-routes
      const publications = await this.controllerFor("publication").publications;
      const latest = decodeId(publications?.at(-1)?.node.id);

      if (latest) {
        this.replaceWith("publication.edit", latest);
      }
    });
  }
}
