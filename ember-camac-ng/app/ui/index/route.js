import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class IndexRoute extends Route {
  @service shoebox;
  @service router;

  redirect() {
    const { entrypoint = {} } = this.shoebox.content;
    const { path = null, models = [], queryParams = {} } = entrypoint;

    if (!path) return;

    return this.router.replaceWith(path, ...models, { queryParams });
  }
}
