import { module, test } from "qunit";

import { parseNested } from "ember-ebau-core/utils/dms";

module("Unit | Utility | dms", function () {
  module("parseNested", function () {
    const locale = "de";

    const aliases = {
      date: [{ de: "datum" }],
      opposing: [{ de: "einsprechende" }],
      "opposing.address": [{ de: "adresse" }],
      user: [{ de: "benutzer" }],
      "user.firstName": [{ de: "vorname" }],
      "user.lastName": [{ de: "nachname" }],
    };

    test("Handle arrays and single objects with nested attributes", function (assert) {
      const item = {
        date: 1,
        datum: 1,
        opposing: [
          {
            address: 1,
            adresse: 1,
          },
          {
            address: 1,
            adresse: 1,
          },
        ],
        einsprechende: [
          {
            address: 1,
            adresse: 1,
          },
          {
            address: 1,
            adresse: 1,
          },
        ],
        user: {
          firstName: "some",
          lastName: "name",
        },
        benutzer: {
          vorname: "some",
          nachname: "name",
        },
      };

      const expectedResult = {
        datum: 1,
        einsprechende: [
          {
            adresse: 1,
          },
          {
            adresse: 1,
          },
        ],
        benutzer: {
          vorname: "some",
          nachname: "name",
        },
      };

      const result = parseNested(item, aliases, locale);
      assert.deepEqual(
        result,
        expectedResult,
        "Map all keys across all elements in an array or a single object",
      );
    });

    test("Handles edge-case payloads gracefully", function (assert) {
      assert.strictEqual(
        parseNested(null, aliases, locale),
        null,
        "Handles null gracefully",
      );
      assert.deepEqual(
        parseNested([], aliases, locale),
        [],
        "Handles an empty array gracefully",
      );
    });
  });
});
