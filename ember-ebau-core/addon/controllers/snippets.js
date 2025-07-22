import Controller from "@ember/controller";
import { dedupeTracked } from "tracked-toolbox";

export default class SnippetsController extends Controller {
  queryParams = ["search"];

  @dedupeTracked search = "";
}
