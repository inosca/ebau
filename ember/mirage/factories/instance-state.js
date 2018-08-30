import { Factory, faker } from "ember-cli-mirage";

const instanceStates = [
  {
    name: "new",
    description: "Neu"
  },
  {
    name: "subm",
    description: "Eingereicht"
  },
  {
    name: "comm",
    description: "Von Gemeinde angenommenen"
  },
  {
    name: "circ",
    description: "In Zirkulation"
  },
  {
    name: "redac",
    description: "Bauentscheid ausstehend"
  },
  {
    name: "nfd",
    description: "Nachforderung"
  },
  {
    name: "done",
    description: "Bewilligt"
  },
  {
    name: "rej",
    description: "Abgelehnt"
  },
  {
    name: "arch",
    description: "Archiviert"
  },
  {
    name: "del",
    description: "Gel\u00f6scht"
  }
];

export default Factory.extend({
  name: faker.list.cycle(...instanceStates.map(({ name }) => name)),
  description: faker.list.cycle(
    ...instanceStates.map(({ description }) => description)
  )
});
