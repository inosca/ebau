import Component from '@ember/component'
import ActiveLinkMixin from 'ember-cli-active-link-wrapper/mixins/active-link'
import { inject as service } from '@ember/service'
import { computed } from '@ember/object'
import { task } from 'ember-concurrency'
import { all } from 'rsvp'

export default Component.extend(ActiveLinkMixin, {
  questionStore: service(),

  activeClass: 'uk-active',

  questions: computed(
    'module.questions',
    'submodules.@each.questions',
    function() {
      let q = [
        ...this.getWithDefault('module.questions', []),
        ...this.getWithDefault('module.submodules', []).reduce(
          (qs, submodule) => {
            return [...qs, ...submodule.questions]
          },
          []
        )
      ]
      return q
    }
  ),

  visibleQuestions: computed('questions.[]', async function() {}),

  state: computed(
    'questionStore._store.@each.{value,isNew,hidden}',
    function() {
      let task = this.get('_computeState')

      task.perform()

      return task
    }
  ),

  _computeState: task(function*() {
    let names = this.get('questions', [])

    let questions = yield this.get('questionStore.findSet').perform(
      names,
      this.get('instance')
    )

    let visibles = yield all(
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
  })
})
