import { Factory, faker } from 'ember-cli-mirage'

const locations = [
  {
    communalFederalNumber: 1301,
    name: 'Einsiedeln'
  },
  {
    communalFederalNumber: 1311,
    name: 'Gersau'
  },
  {
    communalFederalNumber: 1321,
    name: 'Feusisberg'
  },
  {
    communalFederalNumber: 1322,
    name: 'Freienbach'
  },
  {
    communalFederalNumber: 1323,
    name: 'Wollerau'
  },
  {
    communalFederalNumber: 1331,
    name: 'Küssnacht'
  },
  {
    communalFederalNumber: 1341,
    name: 'Altendorf'
  },
  {
    communalFederalNumber: 1342,
    name: 'Galgenen'
  },
  {
    communalFederalNumber: 1343,
    name: 'Innerthal'
  },
  {
    communalFederalNumber: 1344,
    name: 'Lachen'
  },
  {
    communalFederalNumber: 1345,
    name: 'Reichenburg'
  },
  {
    communalFederalNumber: 1346,
    name: 'Schübelbach'
  },
  {
    communalFederalNumber: 1347,
    name: 'Tuggen'
  },
  {
    communalFederalNumber: 1348,
    name: 'Vorderthal'
  },
  {
    communalFederalNumber: 1349,
    name: 'Wangen'
  },
  {
    communalFederalNumber: 1361,
    name: 'Alpthal'
  },
  {
    communalFederalNumber: 1362,
    name: 'Arth'
  },
  {
    communalFederalNumber: 1363,
    name: 'Illgau'
  },
  {
    communalFederalNumber: 1364,
    name: 'Ingenbohl'
  },
  {
    communalFederalNumber: 1365,
    name: 'Lauerz'
  },
  {
    communalFederalNumber: 1366,
    name: 'Morschach'
  },
  {
    communalFederalNumber: 1367,
    name: 'Muotathal'
  },
  {
    communalFederalNumber: 1368,
    name: 'Oberiberg'
  },
  {
    communalFederalNumber: 1369,
    name: 'Riemenstalden'
  },
  {
    communalFederalNumber: 1370,
    name: 'Rothenthurm'
  },
  {
    communalFederalNumber: 1371,
    name: 'Sattel'
  },
  {
    communalFederalNumber: 1372,
    name: 'Schwyz'
  },
  {
    communalFederalNumber: 1373,
    name: 'Steinen'
  },
  {
    communalFederalNumber: 1374,
    name: 'Steinerberg'
  },
  { communalFederalNumber: 1375, name: 'Unteriberg' }
]

export default Factory.extend({
  communalFederalNumber: faker.list.cycle(
    ...locations.map(({ communalFederalNumber }) => communalFederalNumber)
  ),
  name: faker.list.cycle(...locations.map(({ name }) => name))
})
