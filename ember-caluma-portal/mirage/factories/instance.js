import { Factory, association } from "miragejs";

export default Factory.extend({
  instanceState: association(),
  activeService: association(),
});
