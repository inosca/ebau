import Controller from '@ember/controller'
import EmberObject, { computed, get, getWithDefault } from '@ember/object'
import { gt } from '@ember/object/computed'
import { inject as service } from '@ember/service'
import { task } from 'ember-concurrency'
import { all } from 'rsvp'
import { getOwner } from '@ember/application'
import computedTask from 'citizen-portal/lib/computed-task'

const Module = EmberObject.extend({
  questionStore: service(),

  allQuestions: computed('questions', 'submodules.@each.questions', function() {
    return [
      ...this.getWithDefault('questions', []),
      ...this.getWithDefault('submodules', []).reduce((qs, submodule) => {
        return [...qs, ...getWithDefault(submodule, 'questions', [])]
      }, [])
    ]
  }),

  editable: computed('editableTypes.[]', async function() {
    let questions = await this.get('questionStore.findSet').perform(
      this.getWithDefault('allQuestions', []),
      this.get('instance')
    )
    let editable = this.getWithDefault('editableTypes', [])

    let editableFieldTypes = [
      ...(editable.includes('form')
        ? [
            'text',
            'number',
            'radio',
            'checkbox',
            'select',
            'multiselect',
            'table',
            'gwr'
          ]
        : []),
      ...(editable.includes('document') ? ['document'] : [])
    ]

    return questions.some(({ field: { type } }) => {
      return editableFieldTypes.includes(type)
    })
  }),

  state: computed(
    'questionStore._store.@each.{value,hidden,isNew}',
    async function() {
      let names = this.getWithDefault('allQuestions', [])

      let questions = await this.get('questionStore.findSet').perform(
        names,
        this.get('instance')
      )

      let visibles = await all(
        questions.map(async q => ((await q.get('hidden')) ? null : q))
      )

      let visibleQuestions = visibles.filter(Boolean)

      if (!visibleQuestions.length) {
        return null
      }

      if (visibleQuestions.every(q => q.get('isNew'))) {
        return 'untouched'
      }

      let relevantQuestions = visibleQuestions.filter(q =>
        q.get('field.required')
      )

      if (relevantQuestions.some(q => q.get('isNew'))) {
        return 'unfinished'
      }

      return relevantQuestions.every(q => q.validate() === true)
        ? 'valid'
        : 'invalid'
    }
  )
})

export default Controller.extend({
  questionStore: service(),
  router: service(),
  ajax: service(),

  modules: computedTask('_modules', 'model.instance.form.name'),
  _modules: task(function*() {
    let { forms, modules } = yield this.get('questionStore.config')

    let usedModules = getWithDefault(
      forms,
      this.get('model.instance.form.name'),
      []
    )
      .map(name => ({ name, ...modules[name] } || null))
      .filter(Boolean)

    return usedModules
      .map(({ name, title, parent, questions }) => {
        return Module.create({
          container: getOwner(this).__container__,

          link: `instances.edit.${name}`,
          instance: this.get('model.instance.id'),
          editableTypes: this.get('model.meta.editable'),
          name,
          title,
          questions,
          parent,
          submodules: []
        })
      })
      .filter(mod => {
        try {
          this.get('router').urlFor(mod.get('link'))
          return true
        } catch (e) {
          // URL does not exist, skip this module
          return false
        }
      })
  }),

  navigation: computed('modules.lastSuccessful.value.[]', function() {
    return this.getWithDefault('modules.lastSuccessful.value', []).reduce(
      (nav, mod) => {
        if (mod.get('parent')) {
          let parent = nav.find(n => n.get('name') === mod.get('parent'))

          parent.set('submodules', [
            ...parent
              .get('submodules')
              .filter(sub => sub.get('name') !== mod.get('name')),
            mod
          ])
        } else {
          nav.push(mod)
        }

        return nav
      },
      []
    )
  }),

  links: computedTask(
    '_links',
    'modules.lastSuccessful.value.[]',
    'questionStore._store.@each.{value,isNew,hidden}'
  ),
  _links: task(function*() {
    return [
      'instances.edit.index',
      ...(yield all(
        this.getWithDefault('modules.lastSuccessful.value', []).map(async m => {
          return (await m.get('state')) ? m.get('link') : null
        })
      )).filter(Boolean),
      ...(this.get('model.meta.editable').includes('form')
        ? ['instances.edit.submit']
        : [])
    ]
  }),

  currentIndex: computed(
    'links.lastSuccessful.value.[]',
    'router.currentRouteName',
    function() {
      return this.getWithDefault('links.lastSuccessful.value', []).indexOf(
        this.get('router.currentRouteName')
      )
    }
  ),

  hasPrev: gt('currentIndex', 0),
  hasNext: computed(
    'links.lastSuccessful.value.length',
    'currentIndex.lastSuccessful.value',
    function() {
      return (
        this.get('currentIndex') <
        this.getWithDefault('links.lastSuccessful.value.length', 0) - 1
      )
    }
  ),

  prev: task(function*() {
    yield this.get('questionStore.saveQuestion.last')

    let links = this.get('links.lastSuccessful.value')
    let i = this.get('currentIndex')

    yield this.transitionToRoute(
      get(links, (i + links.length - 1) % links.length)
    )
  }),

  next: task(function*() {
    yield this.get('questionStore.saveQuestion.last')

    let links = this.get('links.lastSuccessful.value')
    let i = this.get('currentIndex')

    yield this.transitionToRoute(get(links, (i + 1) % links.length))
  })
})
