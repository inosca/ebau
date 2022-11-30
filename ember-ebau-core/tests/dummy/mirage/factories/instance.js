import { faker } from "@faker-js/faker";
import { Factory, trait } from "miragejs";

export default Factory.extend({
  dossierNumber: () => `${faker.random.numeric(5)}-${faker.random.numeric(2)}`,
  withTopics: trait({
    afterCreate(instance, server) {
      server.createList("communications-topic", 5, "withMessages", {
        instance,
      });
    },
  }),
});
