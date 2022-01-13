import { setContext } from "@apollo/client/link/context";
import { inject as service } from "@ember/service";
import CalumaApolloService from "@projectcaluma/ember-core/services/apollo";

export default class CustomCalumaApolloService extends CalumaApolloService {
  @service session;
  @service shoebox;

  link() {
    const httpLink = super.link();

    const middleware = setContext(async (_, context) => ({
      ...context,
      headers: {
        authorization: await this.session.getAuthorizationHeader(),
        "accept-language": this.shoebox.content.language,
        "x-camac-group": this.shoebox.content.groupId,
        ...context.headers,
      },
    }));

    return middleware.concat(httpLink);
  }
}
