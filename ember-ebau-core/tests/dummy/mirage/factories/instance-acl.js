import { faker } from "@faker-js/faker";
import { Factory, association, trait } from "miragejs";

// ATTENTION: This file is soft linked to ../ember-camac-ng/mirage/factories/ to prevent dublicated code!!!

export default Factory.extend({
  // TODO: refactor token handling
  token: () => faker.git.commitSha(),

  createdAt: () => faker.date.past(),
  revokedAt: () => faker.helpers.maybe(faker.date.recent, { probability: 0.2 }),
  startTime: () => faker.date.past(),

  user: association(),
  service: association(),
  instance: association(),
  createdByUser: association(),
  createdByService: association(),

  afterCreate: (instanceAcl, server) => {
    const accessLevel =
      faker.helpers.arrayElement(server.schema.accessLevels.all()?.models) ??
      server.create("access-level");

    instanceAcl.update({
      accessLevel,
      grantType: accessLevel.requiredGrantType,
      endTime: instanceAcl.revokedAt ?? faker.helpers.maybe(faker.date.future),
      status: instanceAcl.revokedAt ? "expired" : "active",
      entityName: `${instanceAcl.user.name} ${instanceAcl.user.surname}`,
    });
    if (instanceAcl.revokedAt) {
      if (instanceAcl.createdByUser) {
        instanceAcl.update({
          revokedByUser: server.create("user"),
        });
      } else {
        instanceAcl.update({
          revokedByService: instanceAcl.createdByService,
        });
      }
    }
  },

  expired: trait({
    revokedAt: (instance) => instance.endTime ?? faker.date.recent(),
    status: "expired",
  }),

  scheduled: trait({
    startTime: () => faker.date.future(),
    status: "scheduled",
  }),

  active: trait({
    endTime: null,
    revokedAt: null,
    revokedByUser: null,
    status: "active",
  }),
});
