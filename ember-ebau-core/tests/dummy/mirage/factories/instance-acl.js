import { faker } from "@faker-js/faker";
import { Factory, association, trait } from "miragejs";

// ATTENTION: This file is soft linked to ../ember-camac-ng/mirage/factories/ to prevent duplicated code!!!

export default Factory.extend({
  // TODO: refactor token handling
  token: () => faker.git.commitSha(),

  createdAt: () => faker.date.past(),
  startTime: () => faker.date.past(),
  endTime: () => faker.helpers.maybe(faker.date.recent, { probability: 0.2 }),

  user: association(),
  service: association(),
  instance: association(),
  createdByUser: association(),
  createdByService: association(),

  expired: trait({
    endTime: (instance) => instance.endTime ?? faker.date.recent(),
    status: "expired",
  }),

  scheduled: trait({
    startTime: () => faker.date.future(),
    endTime: null,
    status: "scheduled",
  }),

  active: trait({
    endTime: null,
    revokedAt: null,
    revokedByUser: null,
    status: "active",
  }),

  afterCreate: (instanceAcl, server) => {
    const existingAccessLevels = server.schema.accessLevels.all()?.models;
    const accessLevel = existingAccessLevels.length
      ? faker.helpers.arrayElement(existingAccessLevels)
      : server.create("access-level");

    instanceAcl.update({
      accessLevel,
      grantType: accessLevel.requiredGrantType,
    });

    if (instanceAcl.revokedAt) {
      if (instanceAcl.createdByUser) {
        instanceAcl.update({
          revokedByUser: instanceAcl.createdByUser,
        });
      } else {
        instanceAcl.update({
          revokedByService: instanceAcl.createdByService,
        });
      }
    }
  },
});
