import graphqlHandler from "@projectcaluma/ember-testing/mirage-graphql";
import { discoverEmberDataModels } from "ember-cli-mirage";
import { createServer } from "miragejs";

export default function makeServer(config) {
  return createServer({
    ...config,
    models: { ...discoverEmberDataModels(), ...config.models },
    routes() {
      this.timing = 400;

      this.get("/api/v1/instances/:id");

      this.get("/api/v1/users/");

      this.get("/api/v1/services");
      this.get("/api/v1/services/:id");
      this.patch("/api/v1/services/:id");

      this.get("/api/v1/history-entries");

      this.get("/api/v1/journal-entries");
      this.post("/api/v1/journal-entries");
      this.get("/api/v1/journal-entries/:id");
      this.patch("/api/v1/journal-entries/:id");

      this.get("/api/v1/responsible-services");
      this.post("/api/v1/responsible-services");
      this.patch("/api/v1/responsible-services/:id");

      this.get("/api/v1/notification-templates");

      this.get("/api/v1/groups/:id");

      this.get("/api/v1/dossier-imports");
      this.get("/api/v1/dossier-imports/:id");
      this.delete("/api/v1/dossier-imports/:id");
      // Ignore uploaded zip file
      this.post(
        "/api/v1/dossier-imports",
        function ({ dossierImports, users }) {
          return dossierImports.create({ user: users.first() });
        }
      );

      this.post("/graphql/", graphqlHandler(this), 200);

      this.passthrough("/index/token");
    },
  });
}
