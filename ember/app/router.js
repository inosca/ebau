import EmberRouter from '@ember/routing/router'
import config from './config/environment'

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
})

Router.map(function() {
  this.route('login')

  this.route('protected', { path: '/' }, function() {
    this.route('index', { path: '/', resetNamespace: true })
  })
})

export default Router
