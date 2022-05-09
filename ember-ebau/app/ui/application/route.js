import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class ApplicationRoute extends Route {
  @service session;

  async beforeModel(transition) {
    super.beforeModel(transition);

    await this.session.setup();

    // trigger the setter to initialize i18n
    // TODO: the initialization might be better placed in the session setup hook
    // eslint-disable-next-line no-self-assign
    this.session.language = this.session.language;
  }
}
