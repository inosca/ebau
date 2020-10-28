import Service from "@ember/service";
import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

const SHOEBOX_CONTENT = { foo: "bar" };

class StubDocumentService extends Service {
  querySelector() {
    return {
      innerHTML: JSON.stringify(SHOEBOX_CONTENT),
    };
  }
}

module("Unit | Service | shoebox", function (hooks) {
  setupTest(hooks);

  hooks.beforeEach(function () {
    this.owner.register("service:-document", StubDocumentService);
  });

  test("it parses the shoebox", function (assert) {
    const service = this.owner.lookup("service:shoebox");

    assert.deepEqual(service.content, SHOEBOX_CONTENT);
  });
});
