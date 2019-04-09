import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import ApolloService from "ember-apollo-client/services/apollo";
import { setContext } from "apollo-link-context";
import CalumaApolloServiceMixin from "ember-caluma/mixins/caluma-apollo-service-mixin";

export default ApolloService.extend(CalumaApolloServiceMixin, {
  session: service(),

  link: computed("session.data.authenticated.access_token", function() {
    const httpLink = this._super(...arguments);

    const authMiddleware = setContext(async () => {
      const token = this.get("session.data.authenticated.access_token");
      return { headers: { authorization: `Bearer ${token}` } };
    });

    return authMiddleware.concat(httpLink);
  })
});
