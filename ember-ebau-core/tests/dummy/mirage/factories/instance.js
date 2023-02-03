import { Factory, trait } from "miragejs";

export default Factory.extend({
  withTopics: trait({
    afterCreate(instance, server) {
      server.createList("communications-topic", 5, "withMessages", {
        instance,
      });
    },
  }),
});
