import Route from "@ember/routing/route";

export default class CasesDetailCommunicationsDetailRoute extends Route {
  model({ topic_id }) {
    return topic_id;
  }
}
