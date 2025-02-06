import Controller from "@ember/controller";
import { tracked } from "@glimmer/tracking";

export default class SnippetsAdminNewController extends Controller {
  queryParams = ["category"];

  @tracked category = null;
}
