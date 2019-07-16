import { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import ApolloService from "ember-apollo-client/services/apollo";
import { setContext } from "apollo-link-context";
import { onError } from "apollo-link-error";
import CalumaApolloServiceMixin from "ember-caluma/mixins/caluma-apollo-service-mixin";

export default ApolloService.extend(CalumaApolloServiceMixin, {
  session: service(),
  router: service(),

  token: reads("session.data.authenticated.access_token"),
  group: reads("router.currentRoute.queryParams.group"),
  role: reads("router.currentRoute.queryParams.role"),

  link: computed("token", "group", "role", function() {
    const httpLink = this._super(...arguments);

    const middleware = setContext(async (request, context) => {
      context.headers = Object.assign({}, context.headers, {
        authorization: `Bearer ${this.token}`,
        ...(this.group ? { "x-camac-group": this.group } : {}),
        ...(this.role ? { "x-camac-role": this.role } : {})
      });
      return context;
    });

    const afterware = onError(error => {
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

    return middleware.concat(afterware).concat(httpLink);
  })
});
