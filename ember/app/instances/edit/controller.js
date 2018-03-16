import Controller from '@ember/controller'
import { computed, getWithDefault, get } from '@ember/object'
import { gte } from '@ember/object/computed'
import { inject as service } from '@ember/service'
import { task } from 'ember-concurrency'
import forms from 'citizen-portal/questions/forms'
import modules from 'citizen-portal/questions/modules'

export default Controller.extend({
  router: service(),

  navigation: computed('model.form.name', function() {
    let moduleConfig = getWithDefault(forms, this.get('model.form.name'), [])

    return moduleConfig.map(
      ({ module: modKey, submodules: submodKeys, questions }) => {
        let mod = modules[modKey]

        return {
          link: `instances.edit.${modKey}`,
          title: mod.title,
          questions,
          submodules: submodKeys.map(submodKey => {
            return {
              link: `instances.edit.${modKey}.${submodKey}`,
              title: mod.submodules[submodKey].title,
              questions: mod.submodules[submodKey].questions
            }
          })
        }
      }
    )
  }),

  links: computed('navigation.[]', function() {
    return this.get('navigation').reduce((flat, { link, submodules }) => {
      return [
        ...flat,
        ...(submodules.length ? [] : [link]),
        ...submodules.map(({ link }) => link)
      ]
    }, [])
  }),

  currentIndex: computed('links.[]', 'router.currentRouteName', function() {
    return this.get('links').indexOf(this.get('router.currentRouteName'))
  }),

  hasPrev: gte('currentIndex', 0),

  hasNext: computed('links.length', 'currentIndex', function() {
    return this.get('currentIndex') < this.get('links.length') - 1
  }),

  prev: task(function*() {
    let links = this.get('links')
    let i = this.get('currentIndex')

    if (i === 0) {
      yield this.transitionToRoute('instances.edit.index')

      return
    }

    yield this.transitionToRoute(
      get(links, (i + links.length - 1) % links.length)
    )
  }),

  next: task(function*() {
    let links = this.get('links')
    let i = this.get('currentIndex')

    let next = get(links, (i + 1) % links.length)

    // TODO: validate whether all fields are valid

    yield this.transitionToRoute(next)
  })
})
