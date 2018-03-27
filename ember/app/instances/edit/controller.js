import Controller from '@ember/controller'
import { computed, get } from '@ember/object'
import { inject as service } from '@ember/service'
import { task } from 'ember-concurrency'

export default Controller.extend({
  router: service(),
  ajax: service(),

  config: computed(async function() {
    return await this.get('ajax').request('/api/v1/form-config')
  }),

  navigation: computed('model.form.name', async function() {
    let { forms, modules } = await this.get('config')

    let usedModules = (forms[this.get('model.form.name')] || [])
      .map(name => ({ name, ...modules[name] } || null))
      .filter(Boolean)

    let n = usedModules.reduce((nav, { name, title, parent, questions }) => {
      let navItem = {
        link: `instances.edit.${name}`,
        name,
        title,
        questions,
        parent,
        submodules: []
      }

      try {
        this.get('router').urlFor(navItem.link)

        if (parent) {
          nav.find(({ name }) => name === parent).submodules.push(navItem)
        } else {
          nav.push(navItem)
        }
      } catch (e) {
        // URL does not exist, skip this module
      }

      return nav
    }, [])
    return n
  }),

  links: computed('navigation.[]', async function() {
    return [
      'instances.edit',
      ...(await this.get('navigation')).reduce((flat, { link, submodules }) => {
        return [...flat, link, ...submodules.map(({ link }) => link)]
      }, []),
      'instances.edit.submit'
    ]
  }),

  currentIndex: computed(
    'links.[]',
    'router.currentRouteName',
    async function() {
      let links = await this.get('links')

      return links.indexOf(
        this.get('router.currentRouteName').replace(/\.index$/, '')
      )
    }
  ),

  hasPrev: computed('currentIndex', async function() {
    return (await this.get('currentIndex')) > 0
  }),

  hasNext: computed('links.length', 'currentIndex', async function() {
    return (
      (await this.get('currentIndex')) <
      (await this.get('links')).get('length') - 1
    )
  }),

  prev: task(function*() {
    let links = yield this.get('links')
    let i = yield this.get('currentIndex')

    yield this.transitionToRoute(
      get(links, (i + links.length - 1) % links.length)
    )
  }),

  next: task(function*() {
    let links = yield this.get('links')
    let i = yield this.get('currentIndex')

    yield this.transitionToRoute(get(links, (i + 1) % links.length))
  })
})
