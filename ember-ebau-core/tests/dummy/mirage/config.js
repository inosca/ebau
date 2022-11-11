import { discoverEmberDataModels } from "ember-cli-mirage";
import { createServer } from "miragejs";

export default function makeServer(config) {
  return createServer({
    ...config,
    models: { ...discoverEmberDataModels(), ...config.models },
    routes() {
      this.urlPrefix = "/api/v1/";
      this.timing = 400;

      this.get("history-entries");
      this.resource("journal-entries");
      this.resource("attachments");
    },
  });
}
