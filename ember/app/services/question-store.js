import Service, { inject as service } from '@ember/service'
import EmberObject, {
  computed,
  getWithDefault,
  defineProperty
} from '@ember/object'
import { reads, equal } from '@ember/object/computed'
import { getOwner } from '@ember/application'
import { A } from '@ember/array'
import { capitalize } from '@ember/string'
import { task } from 'ember-concurrency'
import _validations from 'citizen-portal/questions/validations'
import computedTask from 'citizen-portal/lib/computed-task'
import jexl from 'jexl'

const Question = EmberObject.extend({
  _questions: service('question-store'),

  init() {
    this._super(...arguments)

    if (this.type === 'form-field') {
      defineProperty(this, 'value', reads('model.value'))
      defineProperty(this, 'isNew', reads('model.isNew'))
    } else {
      defineProperty(
        this,
        'value',
        computed('model.@each.path', function() {
          return this.model.mapBy('path')
        }).readOnly()
      )
      defineProperty(this, 'isNew', equal('model.length', 0))
    }

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

  _getModelForAttachment(name, instance) {
    return this.store
      .peekAll('attachment')
      .filterBy('instance.id', instance)
      .filterBy('question', name)
      .sortBy('date')
      .reverse()
      .reduce((res, i) => {
        if (!res.mapBy('name').includes(i.name)) {
          res.push(i)
        }

        return res
      }, [])
      .sortBy('name')
  },

  _getModelForFormField(name, instance) {
    return (
      this.store
        .peekAll('form-field')
        .filterBy('instance.id', instance)
        .findBy('name', name) ||
      this.store.createRecord('form-field', {
        name,
        instance: this.store.peekRecord('instance', instance)
      })
    )
  },

  async buildQuestion(name, instance) {
    let field = getWithDefault(await this.config, `questions.${name}`, {})
    let type = field.type === 'document' ? 'attachment' : 'form-field'

    let model =
      type === 'attachment'
        ? this._getModelForAttachment(name, instance)
        : this._getModelForFormField(name, instance)

    return Question.create({
      // We need to pass the container of the current service to the question
      // object, to allow it to inject other services, since you can not inject
      // services without container context
      container: getOwner(this).__container__,

      instanceId: instance,

      name,
      model,
      field,
      type
    })
  },

  peek(name, instance) {
    return this._store.find(
      q => q.get('name') === name && q.get('instanceId') === instance
    )
  },

  peekSet(names, instance) {
    return this._store.filter(
      q => names.includes(q.get('name')) && q.get('instanceId') === instance
    )
  }
})
