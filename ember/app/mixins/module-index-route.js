import Mixin from '@ember/object/mixin'
import { inject as service } from '@ember/service'

export default Mixin.create({
  questionStore: service(),

  async redirect(_, transition) {
    // The current route name will be the last route or null (if window was
    // freshly loaded) until the transition is done. We use this to check if we
    // need to skip the route forwards or backwards
    let routeBefore = this.get('router.currentRouteName')
    await transition.promise

    let controller = this.controllerFor('instances.edit')
    let links = await controller.get('links').perform()

    // The current route name is now the actual route since we awaited the end
    // of the transition
    let parent = this.get('router.currentRouteName').replace(/\.index$/, '')
    let parentIndex = links.indexOf(parent)
    let direction =
      routeBefore && parentIndex < links.indexOf(routeBefore) ? -1 : 1

    // If the parent is in the navigation and does not have any questions on it,
    // we redirect to the next or previous page depending on where we came from
    if (
      parentIndex > -1 &&
      !(
        (await this.get('questionStore.config')).modules[
          parent.replace(/^instances\.edit\./, '')
        ].questions.length > 0 || false
      )
    ) {
      return this.replaceWith(links[links.indexOf(parent) + direction])
    }
  }
})
