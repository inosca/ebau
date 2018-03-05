import { Factory, faker } from 'ember-cli-mirage'

const forms = [
  { name: 'baugesuch-reklamegesuch', description: 'Baugesuch, Reklamegesuch' },
  { name: 'projektanderung', description: 'Projektänderung' },
  {
    name: 'vorentscheid-gemass-84-pbg',
    description: 'Vorentscheid gemäss §84 PBG'
  },
  { name: 'vorabklarung', description: 'Vorabklärung' },
  {
    name: 'baumeldung-fur-geringfugiges-vorhaben',
    description: 'Baumeldung für geringfügiges Vorhaben'
  },
  { name: 'technische-bewilligung', description: 'Technische Bewilligung' },
  {
    name: 'konzession-fur-wasserentnahme',
    description: 'Konzession für Wasserentnahme'
  },
  {
    name: 'anlassbewilligungen-verkehrsbewilligungen',
    description: 'Anlassbewilligungen / Verkehrsbewilligungen'
  },
  { name: 'plangenehmigungsgesuch', description: 'Plangenehmigungsgesuch' },
  {
    name: 'projektgenehmigungsgesuch-gemass-ss15-strag',
    description: 'Projektgenehmigungsgesuch gemäss §15 StraG'
  }
]

export default Factory.extend({
  name: faker.list.cycle(...forms.map(({ name }) => name)),
  description: faker.list.cycle(...forms.map(({ description }) => description))
})
