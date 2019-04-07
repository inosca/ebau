import Route from "@ember/routing/route";
import OIDCApplicationRouteMixin from "ember-simple-auth-oidc/mixins/oidc-application-route-mixin";
import { inject as service } from "@ember/service";

export default Route.extend(OIDCApplicationRouteMixin, {
  intl: service(),

  beforeModel() {
    this.intl.setLocale(["de-ch", "de-de"]);
  }
});
