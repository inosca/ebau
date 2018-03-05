import { Response } from 'ember-cli-mirage'
import FormConfig from './form-config'

export default function() {
  this.urlPrefix = '' // make this `http://localhost:8080`, for example, if your API is on a different server
  this.namespace = '' // make this `/api`, for example, if your API is namespaced
  this.timing = 400 // delay for each request, automatically set to 0 during testing

  this.passthrough('https://map.geo.sz.ch/**')
  // TODO: Proxy to backend
  this.passthrough('https://cors-anywhere.herokuapp.com/**')

  this.post('/api-token-auth/', function(_, { requestBody }) {
    let { username = null, password = null } = JSON.parse(requestBody)

    if (!username || !password) {
      return new Response(400)
    }

    let exp = new Date().getTime() + 1000 * 60 * 60 * 24 * 7 // 7 days

    let payload = {
      username,
      exp
    }

    return new Response(
      200,
      {},
      {
        token: `${btoa('a')}.${btoa(JSON.stringify(payload))}.${btoa('c')}`
      }
    )
  })

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
