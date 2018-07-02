import Controller from '@ember/controller'
import { task, timeout } from 'ember-concurrency'
import QueryParams from 'ember-parachute'

export const queryParams = new QueryParams({
  group: {
    defaultValue: null,
    refresh: true,
    replace: true
  },
  sort: {
    defaultValue: '-creation_date',
    refresh: true,
    replace: true
  },
  identifier: {
    defaultValue: '',
    refresh: true,
    replace: true
  }
})

export default Controller.extend(queryParams.Mixin, {
  setup() {
    this.data.perform()
  },

  queryParamsDidChange({ shouldRefresh }) {
    if (shouldRefresh) {
      this.data.perform()
    }
  },

  reset(_, isExiting) {
    if (isExiting) {
      this.resetQueryParams()
    }
  },

  data: task(function*() {
    return yield this.store.query('instance', {
      ...this.allQueryParams,
      include: 'form,instance-state,location'
    })
  }).restartable(),

  navigate: task(function*(instance) {
    let group = this.group

    yield this.transitionToRoute('instances.edit', instance.id, {
      queryParams: group ? { group } : {}
    })
  }),

  search: task(function*(term) {
    yield timeout(500)

    this.set('identifier', term)
  }).restartable()
})
