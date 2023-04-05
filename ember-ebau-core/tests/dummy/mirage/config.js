import { discoverEmberDataModels } from "ember-cli-mirage";
import { createServer } from "miragejs";

export default function makeServer(config) {
  return createServer({
    ...config,
    models: { ...discoverEmberDataModels(), ...config.models },
    routes() {
      this.namespace = "/api/v1";
      this.timing = 400;

      this.resource("history-entries", { only: ["index"] });
      this.resource("journal-entries");
      this.resource("attachments");
      this.resource("instances", { only: ["index", "show"] });
      this.resource("instance-states", { only: ["index", "show"] });
      this.resource("services");
      this.resource("users");

      this.resource("communications-topics");
      this.resource("communications-messages");
      this.resource("communications-attachments");
      this.resource("communications-entities");

      this.namespace = ""; // reset namespace
    },
  });
}
