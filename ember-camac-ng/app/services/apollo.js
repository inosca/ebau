import { inject as service } from "@ember/service";
import { setContext } from "apollo-link-context";
import ApolloService from "ember-apollo-client/services/apollo";
import CalumaApolloServiceMixin from "ember-caluma/mixins/caluma-apollo-service-mixin";

export default class CustomApolloService extends ApolloService.extend(
  CalumaApolloServiceMixin
) {
  @service session;
  @service shoebox;

  link(...args) {
    const httpLink = super.link(...args);

    const middleware = setContext(async (_, context) => ({
      ...context,
      headers: { ...context.headers, ...this.headers },
    }));

    return middleware.concat(httpLink);
  }

  get headers() {
    return {
      authorization: `Bearer ${this.session.data.authenticated.access_token}`,
      "accept-language": this.shoebox.content.language,
      "x-camac-group": this.shoebox.content.groupId,
    };
  }
}
