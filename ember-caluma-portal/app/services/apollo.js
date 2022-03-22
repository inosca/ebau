import { inject as service } from "@ember/service";
import CalumaApolloService from "@projectcaluma/ember-core/services/apollo";
import { apolloMiddleware } from "ember-simple-auth-oidc";

export default class CustomCalumaApolloService extends CalumaApolloService {
  @service session;

  link() {
    return apolloMiddleware(super.link(), this.session);
  }
}
