import Controller from "@ember/controller";
import { dedupeTracked } from "tracked-toolbox";

export default class SnippetsAdminIndexController extends Controller {
  queryParams = ["search"];

  @dedupeTracked search = "";
}
