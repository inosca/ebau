import JSONAPIAdapter from "@ember-data/adapter/json-api";
import { inject as service } from "@ember/service";
import OIDCAdapterMixin from "ember-simple-auth-oidc/mixins/oidc-adapter-mixin";

const BaseAdapter = JSONAPIAdapter.extend(OIDCAdapterMixin);

export default class ApplicationAdapter extends BaseAdapter {
  @service session;

  namespace = "api/v1";
}
