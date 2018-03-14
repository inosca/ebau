import EmberRouter from '@ember/routing/router'
import config from './config/environment'

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
})

Router.map(function() {
  this.route('login')
  this.route('app-shell')

  this.route('protected', { path: '/' }, function() {
    this.route('index', { path: '/', resetNamespace: true })
    this.route('instances', { resetNamespace: true }, function() {
      this.route('new', function() {
        this.route('type')
      })
      this.route('edit', { path: '/:instance_id' }, function() {
        this.route('b', { path: 'grundinformationen' }, function() {
          this.route('1', { path: 'lokalisierung' })
          this.route('2', { path: 'kategorisierung' })
          this.route('3', { path: 'allgemeine-informationen-zum-vorhaben' })
          this.route('4', { path: 'ausnahmebewilligungen' })
        })

        this.route('c', { path: '/personalien' }, function() {
          this.route('1', { path: '/grundeigentuemerschaft' })
        })
      })
    })
  })
})

export default Router
