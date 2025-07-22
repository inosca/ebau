import { Factory, association, trait } from "miragejs";

export default Factory.extend({
  sort: (i) => i,
  responsibleUser: association(),

  withApplicationTypes: trait({
    afterCreate(rule, server) {
      rule.update({
        applicationTypes: server.createList("application-type", 1),
      });
    },
  }),

  withMunicipalities: trait({
    afterCreate(rule, server) {
      rule.update({
        municipalities: server.createList("public-service", 5),
      });
    },
  }),
});
