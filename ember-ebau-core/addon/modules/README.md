# How to write an eBau module

Creating eBau module quite simple, there are just a few steps you need to follow:

1. Write your code (routes, controllers, templates, components) in the
   `ember-ebau-core` addon the same way you would do in an app.
2. Create a register function which exposes the routing tree and the needed
   routes, controllers and templates in a module file.
3. Register the module in the applications `router.js` at the desired location
   using that register function. Also, make sure your router calls the
   `registerModules` method of the ebau modules service in the `setupRouter`
   hook.

## The register function

Your new module must provide a register function which makes sure that the
routing tree in each consuming application and the corresponding classes
(routes, controllers, templates) are registered at the correct location.
Normally, this would be done automatically by the ember resolver analyzing our
app re-exports and registering them accordingly. Since we can't be sure that our
module is located at the same place in each app, we need to do the work
ourselves.

However, we already provide helpers to make this as easy as possible for module
authors. The author simply needs to define the routing tree and the location of
the needed classes inside the module:

```js
// ember-ebau-core/modules/my-module.js

import { registerModule } from "ember-ebau-core/modules";

import MyModuleController from "ember-ebau-core/controllers/my-module";
import MyModuleNewController from "ember-ebau-core/controllers/my-module/new";

import MyModuleRoute from "ember-ebau-core/routes/my-module";
import MyModuleNewRoute from "ember-ebau-core/routes/my-module/new";

import MyModuleTemplate from "ember-ebau-core/template/my-module";
import MyModuleNewTemplate from "ember-ebau-core/template/my-module/new";

export default function register(router, options = {}) {
  router.route("my-module", options, function () {
    this.route("new");
  });

  registerModule("my-module", router.parent, options.resetNamespace, {
    routes: {
      "my-module": MyModuleRoute,
      "my-module/new": MyModuleNewRoute,
    },
    controllers: {
      "my-module": MyModuleController,
      "my-module/new": MyModuleNewController,
    },
    templates: {
      "my-module": MyModuleTemplate,
      "my-module/new": MyModuleNewTemplate,
    },
  });
}
```

This register function can now be used in the consuming app like this:

```js
// my-app/router.js

import EmberRouter from "@ember/routing/router";
import { inject as service } from "@ember/service";
import registerMyModule from "ember-ebau-core/modules/my-module";

export default class Router extends EmberRouter {
  @service ebauModules;

  setupRouter(...args) {
    const didSetup = super.setupRouter(...args);

    if (didSetup) {
      this.ebauModules.setupModules();
    }

    return didSetup;
  }

  // ...
}

Router.map(function () {
  this.route("foo", function () {
    registerMyModule(this);
  });
});
```

## Caveats when writing modules

### Routing

Since the module could be located differently in the consuming apps, routing
(e.g. transitions and links) can't be done the same way you'd do in an
application or an engine. To help with that, eBau modules provide a helper
function for templates and a service method to resolve to the correct route name
in each consuming application:

In templates:

```diff
- <LinkTo @route="my-module.edit">My Link</LinkTo>
+ <LinkTo @route={{module-route "my-module" "edit"}}>My Link</LinkTo>
```

In routes, controllers and components:

```diff
- this.router.transitionTo("my-module.edit");
+ this.router.transitionTo(this.ebauModules.resolveModuleRoute("my-module", "edit"));
```

Using these helpers, a module located once at `"/foo/bar"` and once at `"/baz"`
will resolve to "`/foo/bar/my-module/edit`" for the first case and to
`"/baz/my-module/edit"` for the second case.

### General application information

There is certain information each application is using but doesn't store at the
same location. The best example for this is the current service ID. In
`ember-ebau` this information is stored on the session store but in
`ember-camac-ng` it's stored in the shoebox service.

In order to write code that works in both environments, we require the module
author to take that information from the `ebauModules` service. This service is
being overwritten in each application to act as a proxy to the correct
information in the respective environment.

```diff
- const serviceId = this.shoebox.content.serviceId;
+ const serviceId = this.ebauModules.serviceId;
```

```diff
- const serviceId = this.session.service.id;
+ const serviceId = this.ebauModules.serviceId;
```
