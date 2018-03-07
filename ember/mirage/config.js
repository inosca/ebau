import FormConfig from './form-config'
import keycloakConfig from './keycloak-config'

export default function() {
  this.urlPrefix = '' // make this `http://localhost:8080`, for example, if your API is on a different server
  this.namespace = '' // make this `/api`, for example, if your API is namespaced
  this.timing = 400 // delay for each request, automatically set to 0 during testing

  this.passthrough('https://map.geo.sz.ch/**')
  // TODO: Proxy to backend
  this.passthrough('https://cors-anywhere.herokuapp.com/**')

  keycloakConfig.apply(this)

  this.get('/api/v1/forms')

  this.get('/api/v1/instances')
  this.post('/api/v1/instances')
  this.get('/api/v1/instances/:id')
  this.patch('/api/v1/instances/:id')

  this.get('/api/v1/form-fields')
  this.post('/api/v1/form-fields')
  this.get('/api/v1/form-fields/:id')
  this.patch('/api/v1/form-fields/:id')

  this.get('/api/v1/form-config', function() {
    return FormConfig
  })
}
