import { faker } from "@faker-js/faker";
import { Factory, association } from "miragejs";

export default Factory.extend({
  id: () => faker.string.uuid({ version: 7 }),
  status: () =>
    faker.helpers.arrayElement([
      "pending",
      "confirmed",
      "canceled",
      "invalidated",
    ]),
  roles: () =>
    faker.helpers.arrayElements(
      ["Applicant", "Landowner", "Project author", "Invoice recipient"],
      { min: 1, max: 3 },
    ),
  displayName() {
    return this.user ? this.user.fullName : faker.internet.email();
  },
  createdAt: () => faker.date.past(),
  closedAt() {
    const from = this.createdAt.getTime();
    const to = Date.now();

    return this.status === "pending" ? null : faker.date.between({ from, to });
  },

  user: association(),
  round: association(),
});
