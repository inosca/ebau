import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import OIDCApplicationRouteMixin from "ember-simple-auth-oidc/mixins/oidc-application-route-mixin";
import moment from "moment";

export default class ApplicationRoute extends Route.extend(
  OIDCApplicationRouteMixin
) {
  @service intl;
  @service session;

  beforeModel() {
    moment.locale("de-ch");
    this.intl.setLocale("de");
    /**
     * Reset ebauGroup to prevent sending it if not needed and clean up leftover
     * data. The routes which need it handle it themself.
     */
    this.session.set("data.ebauGroup", undefined);
  }
}
