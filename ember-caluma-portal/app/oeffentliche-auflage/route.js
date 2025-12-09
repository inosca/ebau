import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class OeffentlicheAuflageRoute extends Route {
  @service router;
  @service intl;
  @service session;

  beforeModel() {
    this.intl.setLocale("de");
    this.session.language = "de";
    this.router.transitionTo("public-instances");
  }
}
