import EmberRouter from '@ember/routing/router'
import config from './config/environment'

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
})

Router.map(function() {
  this.route('login')
  this.route('app-shell')
  this.route('notfound', { path: '/*path' })

  this.route('protected', { path: '/' }, function() {
    this.route('index', { path: '/', resetNamespace: true })
    this.route('instances', { resetNamespace: true }, function() {
      this.route('new')
      this.route('edit', { path: '/:instance_id' }, function() {
        this.route('grundinformationen', function() {
          this.route('lokalisierung')
          this.route('kategorisierung')
          this.route('gwr')
          this.route('allgemeine-informationen-zum-vorhaben')
          this.route('ausnahmebewilligungen')
        })
        this.route('personalien', function() {
          this.route('grundeigentumerschaft')
          this.route('bauherrschaft')
          this.route('projektverfasser-planer')
          this.route('gesuchsteller')
          this.route('konzessionsnehmer')
          this.route('bewilligungsnehmer')
        })
        this.route('fachthemen')
        this.route('gesuchsunterlagen')
        this.route('anlassbewilligungen-verkehrsbewilligungen')
        this.route('baumeldung-fur-geringfugige-vorhaben')
        this.route('konzession-fur-wasserentnahme')
        this.route('projektanderung')
        this.route('projektgenehmigungsgesuch')
        this.route('plangenehmigungsverfahren')
        this.route('technische-bewilligung')
        this.route('vorabklarung')
        this.route('vorentscheid')
        this.route('submit')
      })
    })
  })
})

export default Router
