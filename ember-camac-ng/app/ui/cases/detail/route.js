import Route from "@ember/routing/route";

export default class CasesDetailRoute extends Route {
  model({ case_id }) {
    return case_id;
  }
}
