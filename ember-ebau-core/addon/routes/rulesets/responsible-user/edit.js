import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class RulesetsResponsibleUserEditRoute extends Route {
  @service store;

  model({ id }) {
    return this.store.findRecord("responsible-user-rule", id, {
      include: "responsible_user,municipalities,application_types",
    });
  }
}
