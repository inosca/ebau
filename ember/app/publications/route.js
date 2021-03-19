import Route from "@ember/routing/route";
import ENV from "citizen-portal/config/environment";

export default class PublicationsRoute extends Route {
  beforeModel(transition) {
    if (!ENV.APP.showPublications) {
      transition.abort();
    }
  }
}
