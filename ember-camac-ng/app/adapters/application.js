import JSONAPIAdapter from "@ember-data/adapter/json-api";
import { inject as service } from "@ember/service";

export default class ApplicationAdapter extends JSONAPIAdapter {
  @service session;
  @service shoebox;

  namespace = "api/v1";
  useFetch = true;

  async _fetchRequest(options) {
    options.headers = {
      ...options.headers,
      authorization: await this.session.getAuthorizationHeader(),
      "accept-language": this.shoebox.content.language,
      "x-camac-group": this.shoebox.content.groupId,
    };

    return await super._fetchRequest(options);
  }
}
