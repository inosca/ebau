import Service, { inject as service } from '@ember/service'
import EmberObject, { computed, getWithDefault } from '@ember/object'
import { reads } from '@ember/object/computed'
import { getOwner } from '@ember/application'
import { A } from '@ember/array'
import { capitalize } from '@ember/string'
import { task } from 'ember-concurrency'
import _validations from 'citizen-portal/questions/validations'
import computedTask from 'citizen-portal/lib/computed-task'
import jexl from 'jexl'

const Question = EmberObject.extend({
  _questions: service('question-store'),

  name: null,
  field: null,
  model: null,

  value: computed('model.{value,path}', 'field.type', function() {
    return this.get('field.type') === 'document'
      ? this.get('model.path')
      : this.get('model.value')
  }),

  isNew: reads('model.isNew'),

  init() {
    this._super(...arguments)

    this.set('jexl', new jexl.Jexl())

    this.jexl.addTransform('value', question => {
      let q = this._questions.peek(question, this.get('model.instance.id'))

      return q && q.value
    })

    this.jexl.addTransform(
      'mapby',
      (arr, key) => Array.isArray(arr) && arr.map(obj => obj[key])
    )
  },

  validate() {
    let name = this.name
    let { type, required: isRequired = false, config = {} } = this.field

    let validations = [
      isRequired
        ? this.getWithDefault(
            '_questions._validations.validateRequired',
            () => true
          )
        : () => true,
      this.getWithDefault(
        `_questions._validations.validate${capitalize(type)}`,
        () => true
      ),
      this.getWithDefault(`_questions._validations.${name}`, () => true)
    ]

    let isValid = validations.map(fn => fn(config, this.value))

    return (
      isValid.every(v => v === true) ||
      isValid.filter(v => typeof v === 'string')
    )
  },

  hidden: reads('_hidden.lastSuccessful.value'),
  _hidden: computedTask('_hiddenTask', '_questions._store.@each.value'),
  _hiddenTask: task(function*() {
    let expression = this.get('field.active-expression')

    return expression ? !(yield this.jexl.eval(expression)) : false
  })
})

export default Service.extend({
  _validations,

  ajax: service(),
  store: service(),
  router: service(),

  init() {
    this._super(...arguments)

    this.clear()
  },

  clear() {
    this.set('_store', A())
  },

  config: computed(function() {
    return this.ajax.request('/api/v1/form-config')
  }),

  saveQuestion: task(function*(question) {
    yield question

    let validity = question.validate()

    if (validity === true) {
      yield question.get('model').save()

      return null
    }

    return validity
  }),

  async buildQuestion(name, instance) {
    let field = getWithDefault(await this.config, `questions.${name}`, {})
    let type = field.type === 'document' ? 'attachment' : 'form-field'

    let model =
      this.store
        .peekAll(type)
        .find(
          m => (m.name || '').replace(/\.(png|jp(e)?g|pdf)$/, '') === name
        ) ||
      this.store.createRecord(type, {
        name,
        instance: this.store.peekRecord('instance', instance)
      })

    return Question.create({
      // We need to pass the container of the current service to the question
      // object, to allow it to inject other services, since you can not inject
      // services without container context
      container: getOwner(this).__container__,

      name,
      model,
      field
    })
  },

  peek(name, instance) {
    return this._store.find(
      q => q.get('name') === name && q.get('model.instance.id') === instance
    )
  },

  peekSet(names, instance) {
    return this._store.filter(
      q =>
        names.includes(q.get('name')) && q.get('model.instance.id') === instance
    )
  }
})
