import Route from "@ember/routing/route";
import OIDCApplicationRouteMixin from "ember-simple-auth-oidc/mixins/oidc-application-route-mixin";
import moment from "moment";

export default Route.extend(OIDCApplicationRouteMixin, {
  beforeModel() {
    moment.locale("de-ch");
  },
});
