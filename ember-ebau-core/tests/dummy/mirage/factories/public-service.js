import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  name: () => faker.company.name(),
  afterCreate(publicService, server) {
    publicService.update({
      serviceGroup: server.create("public-service-group"),
    });
  },
});
