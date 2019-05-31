import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import ApolloService from "ember-apollo-client/services/apollo";
import { setContext } from "apollo-link-context";
import { onError } from "apollo-link-error";
import CalumaApolloServiceMixin from "ember-caluma/mixins/caluma-apollo-service-mixin";

export default ApolloService.extend(CalumaApolloServiceMixin, {
  session: service(),
  router: service(),

  link: computed("session.data.authenticated.access_token", function() {
    const httpLink = this._super(...arguments);

    const authMiddleware = setContext(async (request, context) => {
      const token = this.get("session.data.authenticated.access_token");
      context.headers = Object.assign({}, context.headers, {
        authorization: `Bearer ${token}`
      });
      return context;
    });

    const authAfterware = onError(error => {
      const { networkError, graphQLErrors } = error;

      if (
        (graphQLErrors &&
          graphQLErrors.some(({ message }) =>
            /^401 Client Error/.test(message)
          )) ||
        (networkError && networkError.statusCode === 401)
      ) {
        this.router.transitionTo("logout");
      }
    });

    return authMiddleware.concat(authAfterware).concat(httpLink);
  })
});
