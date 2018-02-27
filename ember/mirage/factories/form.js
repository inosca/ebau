import { Factory, faker } from 'ember-cli-mirage'

const forms = [
  { name: 'Baugesuch, Reklamegesuch' },
  { name: 'Projektänderung' },
  { name: 'Vorentscheid gemäss §84 PBG' },
  { name: 'Vorabklärung' },
  { name: 'Baumeldung für geringfügiges Vorhaben' },
  { name: 'Technische Bewilligung' },
  { name: 'Konzession für Wasserentnahme' },
  { name: 'Anlassbewilligungen / Verkehrsbewilligungen' },
  { name: 'Plangenehmigungsgesuch' },
  { name: 'Projektgenehmigungsgesuch gemäss §15 StraG' }
]

export default Factory.extend({
  name: faker.list.cycle(...forms.map(({ name }) => name))
})
