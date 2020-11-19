import Route from "@ember/routing/route";

export default class HistoryRoute extends Route {
  model({ instance_id: id }) {
    return { id };
  }
}
