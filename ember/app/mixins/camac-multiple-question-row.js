import { computed } from "@ember/object";
import Mixin from "@ember/object/mixin";
import { capitalize } from "@ember/string";
import _validations from "citizen-portal/questions/validations";
import Changeset from "ember-changeset";
import { task } from "ember-concurrency";
import { resolve } from "rsvp";

export default Mixin.create({
  _validations,

  _value: computed("value", "columns.[]", function () {
    return new Changeset(
      this.value || {},
      (...args) => this._validate(...args),
      this.columns.reduce((map, f) => {
        return { ...map, [f.name]: () => this._validate };
      }, {})
    );
  }),

  _validate({ key, newValue }) {
    try {
      const { type, required: isRequired, config } = this.columns.find(
        (f) => f.name === key
      );

      const validations = [
        isRequired
          ? this.getWithDefault("_validations.validateRequired", () => true)
          : () => true,
        this.getWithDefault(
          `_validations.validate${capitalize(type)}`,
          () => true
        ),
        this.getWithDefault(
          `_validations.${this.parentName}/${key}`,
          () => true
        ),
      ];

      const isValid = validations.map((fn) => fn(config, newValue));

      return (
        isValid.every((v) => v === true) ||
        isValid.filter((v) => typeof v === "string")
      );
    } catch (e) {
      return true;
    }
  },

  save: task(function* () {
    const changeset = this._value;

    yield changeset.validate();

    if (changeset.get("isValid")) {
      changeset.execute();

      yield resolve(this.getWithDefault("attrs.on-save", () => {})(this.value));
    }
  }),

  actions: {
    change(name, value) {
      this.set(`_value.${name}`, value);
    },
  },
});
