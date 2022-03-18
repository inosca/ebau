import { setContext } from "@apollo/client/link/context";
import { onError } from "@apollo/client/link/error";
import { inject as service } from "@ember/service";
import CalumaApolloService from "@projectcaluma/ember-core/services/apollo";

export default class CustomCalumaApolloService extends CalumaApolloService {
  @service session;

  link() {
    const httpLink = super.link();

    const middleware = setContext(async (_, context) => {
      await this.session.refreshAuthentication.perform();

      return {
        ...context,
        headers: { ...context.headers, ...this.session.headers },
      };
    });

    const afterware = onError((error) => {
      if (error.networkError && error.networkError.statusCode === 401) {
        this.session.handleUnauthorized();
      }
    });

    return middleware.concat(afterware).concat(httpLink);
  }
}
