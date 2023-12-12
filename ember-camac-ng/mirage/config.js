import graphqlHandler from "@projectcaluma/ember-testing/mirage-graphql";
import { discoverEmberDataModels } from "ember-cli-mirage";
import applyTestQueryParamsFilter from "ember-ebau-core/utils/apply-test-query-params-filter";
import { createServer } from "miragejs";

export default function makeServer(config) {
  return createServer({
    ...config,
    models: { ...discoverEmberDataModels(config.store), ...config.models },
    routes() {
      this.namespace = "/api/v1";
      this.timing = 400;
      this.logging = true;

      this.resource("access-levels", { only: ["index"] });
      this.resource("instances", { only: ["index", "show"] });
      this.resource("users", { only: ["index", "show"] });
      this.resource("public-users");
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

      this.resource("instance-acls", { only: ["index", "show"] });
      this.get("instance-acls", (schema, { queryParams }) => {
        const filtered = applyTestQueryParamsFilter(
          schema.instanceAcls.all(),
          queryParams,
        );
        return filtered;
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
