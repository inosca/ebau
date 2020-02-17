import { getOwner } from "@ember/application";
import Controller from "@ember/controller";
import EmberObject, { computed, get, getWithDefault } from "@ember/object";
import { gt } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import computedTask from "citizen-portal/lib/computed-task";
import { task } from "ember-concurrency";

const Module = EmberObject.extend({
  questionStore: service(),

  queryParams: ["group"],
  group: null,

  allQuestions: computed("questions", "submodules.@each.questions", function() {
    return [
      ...this.getWithDefault("questions", []),
      ...this.getWithDefault("submodules", []).reduce((qs, submodule) => {
        return [...qs, ...getWithDefault(submodule, "questions", [])];
      }, [])
    ];
  }),

  editable: computed("editableTypes.[]", "isApplicant", function() {
    if (!this.isApplicant) {
      return false;
    }

    const questions = this.questionStore.peekSet(
      this.getWithDefault("allQuestions", []),
      this.instance
    );
    const editable = this.getWithDefault("editableTypes", []);

    const editableFieldTypes = [
      ...(editable.includes("form")
        ? ["text", "number", "radio", "checkbox", "table", "gwr"]
        : []),
      ...(editable.includes("document") ? ["document"] : [])
    ];

    return questions.some(({ field: { type } }) => {
      return editableFieldTypes.includes(type);
    });
  }),

  state: computed(
    "questionStore._store.@each.{value,hidden,isNew}",
    function() {
      const names = this.getWithDefault("allQuestions", []);

      const questions = this.questionStore
        .peekSet(names, this.instance)
        .filter(q => !q.hidden);

      if (!questions.length) {
        return null;
      }

      if (questions.every(q => q.get("isNew"))) {
        return "untouched";
      }

      const relevantQuestions = questions.filter(q => q.get("field.required"));

      if (relevantQuestions.some(q => q.get("isNew"))) {
        return "unfinished";
      }

      return relevantQuestions.every(q => q.validate() === true)
        ? "valid"
        : "invalid";
    }
  )
});

export default Controller.extend({
  questionStore: service(),
  router: service(),
  ajax: service(),

  modules: computedTask("_modules", "model.instance.form.name"),
  _modules: task(function*() {
    const { forms, modules } = yield this.get("questionStore.config");

    const usedModules = getWithDefault(
      forms,
      this.get("model.instance.form.name"),
      []
    )
      .map(name => ({ name, ...modules[name] } || null))
      .filter(Boolean);

    return usedModules
      .map(({ name, title, parent, questions }) => {
        return Module.create({
          container: getOwner(this).__container__,

          link: `instances.edit.${name}`,
          instance: this.get("model.instance.id"),
          editableTypes: this.get("model.meta.editable"),
          isApplicant: this.get("model.meta.is-applicant"),
          name,
          title,
          questions,
          parent,
          submodules: []
        });
      })
      .filter(mod => {
        try {
          this.router.urlFor(mod.get("link"));
          return true;
        } catch (e) {
          // URL does not exist, skip this module
          return false;
        }
      });
  }),

  navigation: computed("modules.lastSuccessful.value.[]", function() {
    return this.getWithDefault("modules.lastSuccessful.value", []).reduce(
      (nav, mod) => {
        if (mod.get("parent")) {
          const parent = nav.find(n => n.get("name") === mod.get("parent"));

          parent.set("submodules", [
            ...parent
              .get("submodules")
              .filter(sub => sub.get("name") !== mod.get("name")),
            mod
          ]);
        } else if (!this.get("model.meta.is-applicant")) {
          if (mod.get("name") !== "gesuchsunterlagen") {
            nav.push(mod);
          }
        } else {
          nav.push(mod);
        }

        return nav;
      },
      []
    );
  }),

  links: computed(
    "modules.lastSuccessful.value.[]",
    "questionStore._store.@each.{value,isNew,hidden}",
    function() {
      const editableTypes = ["form", "document"];
      return [
        "instances.edit.index",
        ...this.getWithDefault("modules.lastSuccessful.value", [])
          .filter(({ state }) => Boolean(state))
          .mapBy("link"),
        ...(this.get("model.meta.editable").some(e => editableTypes.includes(e))
          ? ["instances.edit.submit"]
          : [])
      ];
    }
  ),

  currentIndex: computed("links.[]", "router.currentRouteName", function() {
    return this.getWithDefault("links", []).indexOf(
      this.get("router.currentRouteName")
    );
  }),

  hasPrev: gt("currentIndex", 0),
  hasNext: computed(
    "links.length",
    "currentIndex.lastSuccessful.value",
    function() {
      return this.currentIndex < this.getWithDefault("links.length", 0) - 1;
    }
  ),

  currentPage: computed("router.currentRouteName", function() {
    switch (this.get("router.currentRouteName")) {
      case "instances.edit.involvierte-personen":
        return "applicants";
      case "instances.edit.freigegebene-unterlagen":
        return "documents";
      case "instances.edit.publikationsdokumente":
        return "documents";
      default:
        return "form";
    }
  }),

  prev: task(function*() {
    yield this.get("questionStore.saveQuestion.last");

    const links = this.links;
    const i = this.currentIndex;

    yield this.transitionToRoute(
      get(links, (i + links.length - 1) % links.length)
    );
  }),

  next: task(function*() {
    yield this.get("questionStore.saveQuestion.last");

    const links = this.links;
    const i = this.currentIndex;

    yield this.transitionToRoute(get(links, (i + 1) % links.length));
  })
});
