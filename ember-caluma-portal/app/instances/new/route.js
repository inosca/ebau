import Route from "@ember/routing/route";

import { can } from "ember-caluma-portal/-private/decorators";

@can("create instance")
class InstancesNewRoute extends Route {}

export default InstancesNewRoute;
