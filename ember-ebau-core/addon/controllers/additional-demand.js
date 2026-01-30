import Controller from "@ember/controller";
import { service } from "@ember/service";

export default class AdditionalDemandController extends Controller {
  @service session;
  @service additionalDemand;
}
