import Route from "@ember/routing/route";

export default class JournalRoute extends Route {
  model({ instance_id: id }) {
    return { id };
  }
}
