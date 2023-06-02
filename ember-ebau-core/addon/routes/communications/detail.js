import Route from "@ember/routing/route";

export default class CommunicationsDetailRoute extends Route {
  model({ topic_id }) {
    return topic_id;
  }
}
