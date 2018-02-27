import { Factory, association, faker } from 'ember-cli-mirage'

export default Factory.extend({
  creationDate: faker.date.past,
  modificationDate: faker.date.past,
  instanceState: association(),
  previousInstanceState: null,
  form: association(),
  location: association()
})
