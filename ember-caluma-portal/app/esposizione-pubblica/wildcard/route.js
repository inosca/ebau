import Route from "@ember/routing/route";
import { service } from "@ember/service";

import { redirectPublicInstances } from "caluma-portal/router";

export default class EsposizionePubblicaWildcardRoute extends Route {
  @service router;
  @service intl;
  @service session;

  beforeModel() {
    this.intl.setLocale("de");
    this.session.language = "de";
    return redirectPublicInstances(this.router);
  }
}
