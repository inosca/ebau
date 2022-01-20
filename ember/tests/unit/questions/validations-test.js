import validations from "citizen-portal/questions/validations";
import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

const {
  validateRequired,
  validateText,
  validateNumber,
  validateNumberSeparator,
  validateRadio,
  validateCheckbox,
  validateTable,
} = validations;

module("Unit | Validations | questions", function (hooks) {
  setupTest(hooks);

  test("it validates required fields correctly", function (assert) {
    assert.expect(3);

    assert.equal(validateRequired({}, "test"), true);
    assert.equal(
      validateRequired({}, ""),
      "Diese Frage darf nicht leer gelassen werden"
    );
    assert.equal(
      validateRequired({}, null),
      "Diese Frage darf nicht leer gelassen werden"
    );
  });

  test("it validates text fields correctly", function (assert) {
    assert.expect(4);

    assert.equal(validateText({}, ""), true);
    assert.equal(validateText({}, "test"), true);
    assert.equal(
      validateText({ minlength: 3 }, "12"),
      "Der Wert muss mehr als 2 Zeichen lang sein"
    );
    assert.equal(
      validateText({ maxlength: 3 }, "1234"),
      "Der Wert muss weniger als 4 Zeichen lang sein"
    );
  });

  test("it validates number fields correctly", function (assert) {
    assert.expect(5);

    assert.equal(validateNumber({}, ""), true);
    assert.equal(validateNumber({}, "1"), true);
    assert.equal(validateNumber({}, "test"), "Der Wert muss eine Zahl sein");
    assert.equal(
      validateNumber({ min: 3 }, "2"),
      "Der Wert muss grösser als 2 sein"
    );
    assert.equal(
      validateNumber({ max: 3 }, "4"),
      "Der Wert muss kleiner als 4 sein"
    );
  });

  test("it validates number separator fields correctly", function (assert) {
    assert.expect(5);

    assert.equal(validateNumberSeparator({}, ""), true);
    assert.equal(validateNumberSeparator({}, "1"), true);
    assert.equal(
      validateNumberSeparator({}, "test"),
      "Der Wert muss eine Zahl sein"
    );
    assert.equal(
      validateNumberSeparator({ min: 3 }, "2"),
      "Der Wert muss grösser als 2 sein"
    );
    assert.equal(
      validateNumberSeparator({ max: 3 }, "4"),
      "Der Wert muss kleiner als 4 sein"
    );
  });

  test("it validates radio fields correctly", function (assert) {
    assert.expect(2);

    const options = ["option 1", "option 2", "option 3"];

    assert.equal(validateRadio({ options }, "option 1"), true);
    assert.equal(
      validateRadio({ options }, "test"),
      "Der Wert muss in den vorgegebenen Optionen vorhanden sein"
    );
  });

  test("it validates checkbox fields correctly", function (assert) {
    assert.expect(4);

    const options = ["option 1", "option 2", "option 3"];

    assert.equal(validateCheckbox({ options }, ["option 1"]), true);
    assert.equal(validateCheckbox({ options }, ["option 1", "option 2"]), true);
    assert.equal(
      validateCheckbox({ options }, ["test"]),
      "Die Werte müssen in den vorgegebenen Optionen vorhanden sein"
    );
    assert.equal(
      validateCheckbox({ options }, ["test 1", "test 2"]),
      "Die Werte müssen in den vorgegebenen Optionen vorhanden sein"
    );
  });

  test("it validates table fields correctly", function (assert) {
    assert.expect(5);

    // incorrect value
    let columns = [
      { name: "f1", label: "field 1", type: "text", config: {} },
      {
        name: "f2",
        label: "field 2",
        required: true,
        type: "number",
        config: {},
      },
      {
        name: "f3",
        label: "field 3",
        type: "radio",
        config: { options: ["1", "2", "3"] },
      },
      {
        name: "f4",
        label: "field 4",
        required: true,
        type: "checkbox",
        config: { options: ["1", "2", "3"] },
      },
    ];

    let value = [
      {
        f1: "test",
        f2: "test",
        f3: "1",
        f4: ["1", "2"],
      },
    ];

    assert.deepEqual(validateTable({ columns }, value), [
      "field 2: Der Wert muss eine Zahl sein",
    ]);

    // missing required values
    columns = [
      {
        name: "f1",
        label: "field 1",
        required: true,
        type: "text",
        config: {},
      },
      {
        name: "f2",
        label: "field 2",
        required: true,
        type: "number",
        config: {},
      },
      {
        name: "f3",
        label: "field 3",
        required: true,
        type: "radio",
        config: { options: ["1", "2", "3"] },
      },
      {
        name: "f4",
        label: "field 4",
        required: true,
        type: "checkbox",
        config: { options: ["1", "2", "3"] },
      },
    ];

    value = [
      {
        f2: "test",
        f3: "1",
      },
      {
        f4: [],
      },
    ];

    assert.deepEqual(validateTable({ columns }, value), [
      "field 1: Diese Frage darf nicht leer gelassen werden",
      "field 2: Der Wert muss eine Zahl sein",
      "field 2: Diese Frage darf nicht leer gelassen werden",
      "field 3: Diese Frage darf nicht leer gelassen werden",
      "field 4: Diese Frage darf nicht leer gelassen werden",
    ]);

    // correct
    columns = [
      { name: "f1", label: "field 1", type: "text", config: {} },
      {
        name: "f2",
        label: "field 2",
        required: true,
        type: "number",
        config: {},
      },
      {
        name: "f3",
        label: "field 3",
        type: "radio",
        config: { options: ["1", "2", "3"] },
      },
      {
        name: "f4",
        label: "field 4",
        required: true,
        type: "checkbox",
        config: { options: ["1", "2", "3"] },
      },
    ];

    value = [
      {
        f1: "test",
        f2: "3",
        f4: ["1", "2"],
      },
      {
        f2: "4",
        f4: ["1"],
      },
    ];

    assert.deepEqual(validateTable({ columns }, value), true);

    // nested arrays
    columns = [
      {
        name: "f1",
        label: "field 1",
        required: true,
        type: "number",
        config: {},
      },
    ];

    value = [
      [
        {
          f1: "1",
        },
      ],
    ];

    assert.deepEqual(validateTable({ columns }, value), true);

    // no table answer
    columns = [
      {
        name: "f1",
        label: "field 1",
        required: true,
        type: "number",
        config: {},
      },
    ];

    assert.deepEqual(validateTable({ columns }, undefined), true);
  });
});
