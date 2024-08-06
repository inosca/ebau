import adapterFactory from "ember-alexandria/adapters/document";

import ApplicationAdapter from "./application";

export default class extends adapterFactory(ApplicationAdapter) {
  get namespace() {
    return "/alexandria/api/v1";
  }
}
