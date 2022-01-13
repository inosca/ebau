import { setContext } from "@apollo/client/link/context";
import { onError } from "@apollo/client/link/error";
import { inject as service } from "@ember/service";
import CalumaApolloService from "@projectcaluma/ember-core/services/apollo";

export default class CustomCalumaApolloService extends CalumaApolloService {
  @service session;

  link() {
    const httpLink = super.link();

    const middleware = setContext(async (_, context) => ({
      ...context,
      headers: { ...context.headers, ...this.session.authHeaders },
    }));

    const afterware = onError((error) => {
      if (error.networkError && error.networkError.statusCode === 401) {
        this.session.handleUnauthorized();
      }
    });

    return middleware.concat(afterware).concat(httpLink);
  }
}
