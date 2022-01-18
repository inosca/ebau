import { getOwner } from "@ember/application";
import { A } from "@ember/array";
import EmberObject, {
  computed,
  getWithDefault,
  defineProperty,
} from "@ember/object";
import { reads, equal } from "@ember/object/computed";
import Service, { inject as service } from "@ember/service";
import { classify } from "@ember/string";
import computedTask from "citizen-portal/lib/computed-task";
import _validations from "citizen-portal/questions/validations";
import { task, timeout } from "ember-concurrency";
import jexl from "jexl";

const traverseTransforms = function* (tree) {
  for (const node of Object.values(tree)) {
    if (typeof node === "object") {
      yield* traverseTransforms(node);
    }
  }
  if (tree.type === "FunctionCall" && tree.pool === "transforms") {
    yield { name: tree.name, args: tree.args };
  }
};

const getTransforms = (tree) => {
  const iterator = traverseTransforms(tree);
  let result = iterator.next();
  const transforms = [];

  while (!result.done) {
    transforms.push(result.value);

    result = iterator.next();
  }

  return transforms;
};

const Question = EmberObject.extend({
  _questions: service("question-store"),

  init(...args) {
    this._super(...args);

    this.set("instanceId", this.get("instance.id"));

    if (this.type === "form-field") {
      defineProperty(this, "value", reads("model.value"));
      defineProperty(this, "isNew", reads("model.isNew"));
    } else {
      defineProperty(
        this,
        "value",
        computed("model.@each.path", function () {
          return this.model.mapBy("path");
        }).readOnly()
      );
      defineProperty(this, "isNew", equal("model.length", 0));
    }

    this.set("jexl", new jexl.Jexl());

    this.jexl.addTransform("value", (question) => {
      const q = this._questions.peek(question, this.get("instance.id"));

      return q && q.value;
    });

    this.jexl.addTransform(
      "mapby",
      (arr, key) => Array.isArray(arr) && arr.map((obj) => obj[key])
    );
  },

  _expressionAST: computed("field.active-expression", function () {
    const expression = this.get("field.active-expression");

    if (!expression) {
      return [];
    }

    return this.jexl.createExpression(expression)._getAst();
  }),

  _relatedQuestionNames: computed("_expressionAST", function () {
    return [
      ...new Set(
        getTransforms(this._expressionAST)
          .filter(({ name }) => name === "value")
          .map((transform) => transform.args[0].value)
      ),
    ];
  }),

  _relatedQuestions: computed(
    "_relatedQuestionNames.[]",
    "instanceId",
    function () {
      return this._questions.peekSet(
        this._relatedQuestionNames,
        this.instanceId
      );
    }
  ),

  _relatedHidden: computed("_relatedQuestions.@each.hidden", function () {
    if (!this._relatedQuestions.length) {
      return false;
    }

    return this._relatedQuestions.every((q) => q.hidden);
  }),

  validate() {
    const name = this.name;
    const { type, required: isRequired = false, config = {} } = this.field;

    const validations = [
      isRequired
        ? this.getWithDefault(
            "_questions._validations.validateRequired",
            () => true
          )
        : () => true,
      this.getWithDefault(
        `_questions._validations.validate${classify(type)}`,
        () => true
      ),
      this.getWithDefault(`_questions._validations.${name}`, () => true),
    ];

    const isValid = validations.map((fn) => fn(config, this.value));

    return (
      isValid.every((v) => v === true) ||
      isValid.flat().filter((v) => typeof v === "string")
    );
  },

  hidden: reads("_hidden.lastSuccessful.value"),
  _hidden: computedTask(
    "_hiddenTask",
    "_relatedQuestions.@each.value",
    "_relatedHidden"
  ),
  _hiddenTask: task(function* () {
    yield timeout(100);

    const expression = this.get("field.active-expression");

    return expression
      ? this._relatedHidden ||
          !(yield this.jexl.eval(expression, {
            form: this.get("instance.form.name"),
            state: this.get("instance.instanceState.name"),
          }))
      : false;
  }).restartable(),
});

export default Service.extend({
  _validations,

  ajax: service(),
  store: service(),
  router: service(),

  init(...args) {
    this._super(...args);

    this.clear();
  },

  clear() {
    this.set("_store", A());
  },

  config: computed(function () {
    return this.ajax.request("/api/v1/form-config");
  }),

  saveQuestion: task(function* (question) {
    yield question;

    const validity = question.validate();

    if (validity === true) {
      yield question.get("model").save();

      return null;
    }

    return validity;
  }),

  _getModelForAttachment(name, instance) {
    return this.store
      .peekAll("attachment")
      .filterBy("instance.id", instance)
      .filterBy("question", name)
      .sortBy("date")
      .reverse()
      .reduce((res, i) => {
        if (!res.mapBy("name").includes(i.name)) {
          res.push(i);
        }

        return res;
      }, [])
      .sortBy("name");
  },

  _getModelForFormField(name, instance) {
    return (
      this.store
        .peekAll("form-field")
        .filterBy("instance.id", instance)
        .findBy("name", name) ||
      this.store.createRecord("form-field", {
        name,
        instance: this.store.peekRecord("instance", instance),
      })
    );
  },

  async buildQuestion(name, instance) {
    const field = getWithDefault(await this.config, `questions.${name}`, {});
    const type = field.type === "document" ? "attachment" : "form-field";

    const model =
      type === "attachment"
        ? this._getModelForAttachment(name, instance)
        : this._getModelForFormField(name, instance);

    return Question.create({
      // We need to pass the container of the current service to the question
      // object, to allow it to inject other services, since you can not inject
      // services without container context
      container: getOwner(this).__container__,

      instance: this.store.peekRecord("instance", instance),

      name,
      model,
      field,
      type,
    });
  },

  peek(name, instance) {
    return this._store.find(
      (q) => q.get("name") === name && q.get("instanceId") === instance
    );
  },

  peekSet(names, instance) {
    return this._store.filter(
      (q) => names.includes(q.get("name")) && q.get("instanceId") === instance
    );
  },
});
