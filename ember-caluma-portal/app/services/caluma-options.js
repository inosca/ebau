import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class CustomCalumaOptionsService extends CalumaOptionsService {
  alwaysUseNumberSeparatorWidget = hasFeature(
    "caluma.alwaysUseNumberSeparatorWidget",
  );
}
