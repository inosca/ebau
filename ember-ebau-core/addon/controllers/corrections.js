import Controller from "@ember/controller";
import { findRecord } from "ember-data-resources";

export default class CorrectionsController extends Controller {
  instance = findRecord(this, "instance", () => this.model);
}
