import { setApplication } from "@ember/test-helpers";
import { start } from "ember-qunit";

import Application from "ember-caluma-portal/app";
import config from "ember-caluma-portal/config/environment";

setApplication(Application.create(config.APP));

start();
