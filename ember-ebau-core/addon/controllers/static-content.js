import Controller from "@ember/controller";
import { tracked } from "@glimmer/tracking";

export default class StaticContentController extends Controller {
  queryParams = ["technicalSupport", "myServiceSupport"];

  @tracked technicalSupport = false;
  @tracked myServiceSupport = false;
}
