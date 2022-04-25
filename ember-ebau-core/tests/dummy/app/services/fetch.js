import Service from "@ember/service";

// fetch service stub
export default class DummyFetchService extends Service {
  async fetch() {
    return await { hello: "world" };
  }
}
