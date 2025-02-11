import Service from "@ember/service";
import { waitForPromise } from "@ember/test-waiters";

// fetch service stub
export default class DummyFetchService extends Service {
  fetch(...args) {
    return waitForPromise(fetch(...args));
  }
}
