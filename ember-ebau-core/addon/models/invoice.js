import Model, { attr } from "@ember-data/model";

export default class Invoice extends Model {
  @attr("string") invoiceText;
}
