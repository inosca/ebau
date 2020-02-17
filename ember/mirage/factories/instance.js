import { Factory, association, faker, trait } from "ember-cli-mirage";

export default Factory.extend({
  creationDate: () => faker.date.past(),
  modificationDate: () => faker.date.past(),

  previousInstanceState: null,
  instanceState: association(),
  form: association(),
  location: association(),

  afterCreate(instance) {
    const n = String(instance.location.communalFederalNumber).substr(2, 4);
    const y = String(new Date().getFullYear()).substr(2, 4);
    const i = String(instance.id).padStart(3, 0);

    const identifier = `${n}-${y}-${i}`;

    instance.update({ identifier });
  },

  unsubmitted: trait({
    afterCreate(instance) {
      instance.update({ identifier: null });
    }
  })
});
