import { faker } from "@faker-js/faker";
import { DateTime } from "luxon";
import { Factory, association, trait } from "miragejs";

import commonEntry from "./billing-v2-common-entry";

export default Factory.extend({
  ...commonEntry,
  dateAdded: () => DateTime.fromJSDate(faker.date.past()).toISODate(),
  dateCharged: null,
  releasedForClearing: null,
  entryType: () => faker.helpers.arrayElement(["BEW", "BGL"]),

  group: association(),
  user: association(),
  instance: association(),
  invoice: association(),

  charged: trait({
    afterCreate(entry) {
      entry.update({
        dateCharged: DateTime.fromJSDate(
          faker.date.between({
            from: entry.dateAdded,
            to: DateTime.now().toISODate(),
          }),
        ),
      });
    },
  }),
});
