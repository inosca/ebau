import config from 'ember-get-config'

const { host, realm } = config['ember-simple-auth-keycloak']

export default function() {
  this.post(
    `${host}/auth/realms/${realm}/protocol/openid-connect/token`,
    () => {
      let tokenBody = btoa(
        JSON.stringify({
          exp: Math.round(new Date().getTime() + 30 * 60 * 1000 / 1000)
        })
      )

      return {
        access_token: `access.${tokenBody}.token`,
        refresh_token: `refresh.${tokenBody}.token`
      }
    }
  )

  this.post(
    `${host}/auth/realms/${realm}/protocol/openid-connect/logout`,
    () => {}
  )
}
