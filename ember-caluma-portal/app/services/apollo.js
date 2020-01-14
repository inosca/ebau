import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { setContext } from "apollo-link-context";
import { onError } from "apollo-link-error";
import ApolloService from "ember-apollo-client/services/apollo";
import CalumaApolloServiceMixin from "ember-caluma/mixins/caluma-apollo-service-mixin";

export default ApolloService.extend(CalumaApolloServiceMixin, {
  session: service(),
  router: service(),

  token: reads("session.data.authenticated.access_token"),
  language: reads("session.language"),
  group: reads("session.group"),

  link(...args) {
    const httpLink = this._super(...args);

    const middleware = setContext(async (request, context) => ({
      ...context,
      headers: {
        ...context.headers,
        authorization: `Bearer ${this.token}`,
        "accept-language": this.language,
        ...(this.group ? { "x-camac-group": this.group } : {})
      }
    }));

    const afterware = onError(error => {
      const { networkError } = error;

      if (
        networkError &&
        networkError.statusCode === 401 &&
        this.session.isAuthenticated
      ) {
        this.session.invalidate();
      }
    });

    return middleware.concat(afterware).concat(httpLink);
  }
});
