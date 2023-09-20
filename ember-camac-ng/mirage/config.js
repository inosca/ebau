import graphqlHandler from "@projectcaluma/ember-testing/mirage-graphql";
import { discoverEmberDataModels } from "ember-cli-mirage";
import { createServer } from "miragejs";

export default function makeServer(config) {
  return createServer({
    ...config,
    models: { ...discoverEmberDataModels(), ...config.models },
    routes() {
      this.namespace = "/api/v1";
      this.timing = 400;
      this.logging = true;

      this.resource("instances", { only: ["show"] });
      this.resource("users", { only: ["index"] });
      this.resource("services", { except: ["create"] });
      this.resource("history-entries", { only: ["index"] });
      this.resource("journal-entries");
      this.resource("responsible-services", { except: ["delete"] });
      this.resource("notification-templates", { only: ["index"] });
      this.resource("groups", { only: ["show"] });
      this.resource("dossier-imports", { except: ["create", "update"] });

      // Ignore uploaded zip file
      this.post("dossier-imports", function ({ dossierImports, users }) {
        return dossierImports.create({ user: users.first() });
      });

      this.namespace = ""; // reset namespace

      this.resource("user-groups", {
        path: "/api/v1/user-groups",
        exclude: ["update"],
      });

      this.post("/graphql/", graphqlHandler(this), 200);
      this.passthrough("/index/token");
    },
  });
}
