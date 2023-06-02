import Route from "@ember/routing/route";

export default class TaskFormRoute extends Route {
  model({ task }) {
    return task;
  }
}
