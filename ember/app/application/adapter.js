import DS from "ember-data";
import { inject as service } from "@ember/service";
import OIDCAdapterMixin from "ember-simple-auth-oidc/mixins/oidc-adapter-mixin";

export default DS.JSONAPIAdapter.extend(OIDCAdapterMixin, {
  session: service(),

  namespace: "api/v1"
});
