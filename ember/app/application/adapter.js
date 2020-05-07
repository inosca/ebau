import JSONAPIAdapter from "@ember-data/adapter/json-api";
import { inject as service } from "@ember/service";
import OIDCAdapterMixin from "ember-simple-auth-oidc/mixins/oidc-adapter-mixin";

export default JSONAPIAdapter.extend(OIDCAdapterMixin, {
  session: service(),

  namespace: "api/v1"
});
