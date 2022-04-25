import Service from "@ember/service";

// session service stub
export default class DummySessionService extends Service {
  get isReadOnlyRole() {
    return false;
  }
}
