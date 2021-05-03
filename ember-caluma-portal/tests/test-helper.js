import { setApplication } from "@ember/test-helpers";
import { start } from "ember-qunit";
import * as QUnit from "qunit";
import { setup } from "qunit-dom";

import Application from "caluma-portal/app";
import config from "caluma-portal/config/environment";

setApplication(Application.create(config.APP));

setup(QUnit.assert);

start();
