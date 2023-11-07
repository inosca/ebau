import { Factory, trait, association } from "miragejs";

export default Factory.extend({
  instanceState: association(),

  afterCreate(instance, server) {
    if (!instance.activeServiceId) {
      instance.update({
        activeService: server.create("public-service"),
      });
    }
  },

  withTopics: trait({
    afterCreate(instance, server) {
      server.createList("communications-topic", 5, "withMessages", {
        instance,
      });
    },
  }),
});
