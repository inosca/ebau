import ApplicationAdapter from "./application";

export default class InstanceAdapter extends ApplicationAdapter {
  unlink(model) {
    const url = `${this.buildURL("instance", model.id)}/unlink`;
    return this.ajax(url, "PATCH");
  }
}
