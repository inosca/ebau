import EmberObject, { computed } from "@ember/object";
import ModuleIndexRouteMixin from "citizen-portal/mixins/module-index-route";
import { module, test } from "qunit";
import { setupTest } from "ember-qunit";
import { later } from "@ember/runloop";

module("Unit | Mixin | module-index-route", function(hooks) {
  setupTest(hooks);

  test("it redirects to the right route", async function(assert) {
    assert.expect(6);

    const ModuleIndexRouteObject = EmberObject.extend(ModuleIndexRouteMixin);

    const CONTROLLER = EmberObject.extend({
      links: computed(function() {
        return ["test1", "test2", "test2.testy", "test3", "test3.testy"];
      })
    });

    const SERVICE = EmberObject.extend({
      config: computed(async function() {
        return {
          modules: {
            test1: { questions: [] },
            test2: { questions: [] },
            "test2.testy": { questions: [] },
            test3: { questions: ["test"] },
            "test3.testy": { questions: [] }
          }
        };
      })
    });

    let subject = ModuleIndexRouteObject.create({
      questionStore: SERVICE.create({}),
      router: EmberObject.create({}),
      controllerFor() {
        return CONTROLLER.create();
      },
      replaceWith: name => name
    });

    const transition = EmberObject.extend({
      target: "test2.index",

      init() {
        this._super(...arguments);

        this.set(
          "promise",
          new Promise(resolve => {
            // We need some delay to resolve this, so the mixin can detect the
            // origin route
            later(() => {
              subject.set("router.currentRouteName", this.get("target"));
              resolve();
            });
          })
        );
      }
    });

    subject.set("router.currentRouteName", "test1");

    assert.equal(
      await subject.redirect(null, transition.create()),
      "test2.testy",
      "It redirects to the next module if the transition comes from before"
    );

    subject.set("router.currentRouteName", null);

    assert.equal(
      await subject.redirect(null, transition.create()),
      "test2.testy",
      "It redirects to the next module if the transition comes from nowhere (reload)"
    );

    subject.set("router.currentRouteName", "test2.testy");

    assert.equal(
      await subject.redirect(null, transition.create()),
      "test1",
      "It redirects to the previous module if the transition comes after"
    );

    subject.set("router.currentRouteName", "test2");

    assert.notOk(
      await subject.redirect(
        null,
        transition.create({ target: "test3.index" })
      ),
      "It does not redirect if the module has questions"
    );

    subject.set("router.currentRouteName", null);

    assert.notOk(
      await subject.redirect(
        null,
        transition.create({ target: "test3.index" })
      ),
      "It does not redirect if the module has questions"
    );

    subject.set("router.currentRouteName", "test2.testy");

    assert.notOk(
      await subject.redirect(
        null,
        transition.create({ target: "test3.index" })
      ),
      "It does not redirect if the module has questions"
    );
  });
});
