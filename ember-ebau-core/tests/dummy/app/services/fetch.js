import Service from "@ember/service";

// fetch service stub
export default class DummyFetchService extends Service {
  fetch(...args) {
    return fetch(...args);
  }
}
