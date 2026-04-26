import Route from "@ember/routing/route";
import { next } from "@ember/runloop";
import { service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

export default class PublicationIndexRoute extends Route {
  @service router;
  @service ebauModules;

  redirect(_, transition) {
    next(async () => {
      // eslint-disable-next-line ember/no-controller-access-in-routes
      const controller = this.controllerFor(
        this.ebauModules.resolveModuleRoute("publication", "publication"),
      );

      // this only happens when deleting publication drafts
      if (transition.from?.name === "publication.edit") {
        await controller.refetchPublications.perform();
      }

      const publications = await controller.publications;
      const latest = decodeId(publications?.[publications.length - 1]?.node.id);

      if (latest) {
        this.router.replaceWith(
          this.ebauModules.resolveModuleRoute("publication", "edit"),
          latest,
        );
      }
    });
  }
}
