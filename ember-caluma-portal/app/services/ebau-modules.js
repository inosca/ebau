import { tracked } from "@glimmer/tracking";
import EbauModulesService from "ember-ebau-core/services/ebau-modules";

export default class CustomEbauModulesService extends EbauModulesService {
  @tracked instanceId;
  @tracked onAdditionalDemandComplete = () => {};

  isApplicant = true;
}
