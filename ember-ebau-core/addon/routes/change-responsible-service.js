import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class ChangeResponsibleServiceRoute extends Route {
  @service ebauModules;

  model({ type }) {
    return type;
  }
}
