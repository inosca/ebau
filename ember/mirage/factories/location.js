import { Factory, faker } from 'ember-cli-mirage'

const locations = [
  {
    federalNumber: 1301,
    name: 'Einsiedeln'
  },
  {
    federalNumber: 1311,
    name: 'Gersau'
  },
  {
    federalNumber: 1321,
    name: 'Feusisberg'
  },
  {
    federalNumber: 1322,
    name: 'Freienbach'
  },
  {
    federalNumber: 1323,
    name: 'Wollerau'
  },
  {
    federalNumber: 1331,
    name: 'Küssnacht'
  },
  {
    federalNumber: 1341,
    name: 'Altendorf'
  },
  {
    federalNumber: 1342,
    name: 'Galgenen'
  },
  {
    federalNumber: 1343,
    name: 'Innerthal'
  },
  {
    federalNumber: 1344,
    name: 'Lachen'
  },
  {
    federalNumber: 1345,
    name: 'Reichenburg'
  },
  {
    federalNumber: 1346,
    name: 'Schübelbach'
  },
  {
    federalNumber: 1347,
    name: 'Tuggen'
  },
  {
    federalNumber: 1348,
    name: 'Vorderthal'
  },
  {
    federalNumber: 1349,
    name: 'Wangen'
  },
  {
    federalNumber: 1361,
    name: 'Alpthal'
  },
  {
    federalNumber: 1362,
    name: 'Arth'
  },
  {
    federalNumber: 1363,
    name: 'Illgau'
  },
  {
    federalNumber: 1364,
    name: 'Ingenbohl'
  },
  {
    federalNumber: 1365,
    name: 'Lauerz'
  },
  {
    federalNumber: 1366,
    name: 'Morschach'
  },
  {
    federalNumber: 1367,
    name: 'Muotathal'
  },
  {
    federalNumber: 1368,
    name: 'Oberiberg'
  },
  {
    federalNumber: 1369,
    name: 'Riemenstalden'
  },
  {
    federalNumber: 1370,
    name: 'Rothenthurm'
  },
  {
    federalNumber: 1371,
    name: 'Sattel'
  },
  {
    federalNumber: 1372,
    name: 'Schwyz'
  },
  {
    federalNumber: 1373,
    name: 'Steinen'
  },
  {
    federalNumber: 1374,
    name: 'Steinerberg'
  },
  { federalNumber: 1375, name: 'Unteriberg' }
]

export default Factory.extend({
  federalNumber: faker.list.cycle(
    ...locations.map(({ federalNumber }) => federalNumber)
  ),
  name: faker.list.cycle(...locations.map(({ name }) => name))
})
