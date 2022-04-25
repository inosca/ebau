import { discoverEmberDataModels } from "ember-cli-mirage";
import { createServer } from "miragejs";

export default function makeServer(config) {
  return createServer({
    ...config,
    models: { ...discoverEmberDataModels(), ...config.models },
    routes() {
      this.urlPrefix = "";
      this.timing = 400;

      this.get("/api/v1/journal-entries");
      this.post("/api/v1/journal-entries");
      this.get("/api/v1/journal-entries/:id");
      this.patch("/api/v1/journal-entries/:id");
    },
  });
}
