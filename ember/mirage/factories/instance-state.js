import { Factory, faker } from 'ember-cli-mirage'

const instanceStates = [{ name: 'NEW', description: 'Entwurf' }]

export default Factory.extend({
  name: faker.list.cycle(...instanceStates.map(({ name }) => name)),
  description: faker.list.cycle(
    ...instanceStates.map(({ description }) => description)
  )
})
