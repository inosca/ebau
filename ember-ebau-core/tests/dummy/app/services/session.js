import Service from "@ember/service";
import { tracked } from "@glimmer/tracking";

// session service stub
export default class DummySessionService extends Service {
  @tracked isInternal = false;
  @tracked groups = [];
  @tracked group = null;

  get isReadOnlyRole() {
    return false;
  }

  data = { authenticated: { access_token: "token" } };
}
