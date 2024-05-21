import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class CustomCalumaOptionsService extends CalumaOptionsService {
  useNumberSeparatorWidgetAsDefault = hasFeature(
    "caluma.useNumberSeparatorWidgetAsDefault",
  );
}
