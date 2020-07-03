import JSONAPIAdapter from "@ember-data/adapter/json-api";
import { inject as service } from "@ember/service";

export default class ApplicationAdapter extends JSONAPIAdapter {
  @service session;
  @service shoebox;

  namespace = "api/v1";

  get headers() {
    return {
      authorization: `Bearer ${this.session.data.authenticated.access_token}`,
      "accept-language": this.shoebox.content.language,
      "x-camac-group": this.shoebox.content.groupId
    };
  }
}
