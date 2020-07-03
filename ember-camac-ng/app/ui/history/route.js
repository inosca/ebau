import Route from "@ember/routing/route";

export default class JournalRoute extends Route {
  model({ id }) {
    return id;
  }
}
