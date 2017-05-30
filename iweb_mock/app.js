const express = require('express')
const exphbs = require('express-handlebars')
const request = require('request')
const cookieParser = require('cookie-parser')
const bodyParser = require('body-parser')
const proxy = require('express-http-proxy')
const config = require('config')

const PORT = 4400
const base = config.get('base')
const auth = config.has('httpAuth') ? config.get('httpAuth') : undefined
const app = express()
const camacApi = config.get('camacApi')
app.locals.camacUrl = config.get('camacUrl')
app.locals.base = base

app.use(cookieParser())
app.use(bodyParser())

app.engine('.hbs', exphbs({ defaultLayout: 'portal', extname: '.hbs' }))
app.set('view engine', '.hbs')

app.use(
  '/public',
  proxy(camacApi, {
    forwardPath(req, res) {
      return require('url').parse(`/public${req.url}`).path
    }
  })
)

app.get('/', (req, res) => {
  if (req.cookies.camacSession) {
    res.render('home', {
      hash: req.cookies.camacSession,
      id: req.cookies.portalId
    })
  } else {
    res.render('home', {
      hash: req.cookies.camacSession,
      id: req.cookies.portalId,
      overview: null
    })
  }
})

function authenticate(conf) {
  return auth ? Object.assign({}, conf, { auth }) : conf
}

app.post('/hash', (req, res) => {
  request.post(
    authenticate({
      url: `${camacApi}/portal/user/session/resource-id/248`,
      headers: {
        'X-Auth': '340acc71664cde7b4b6608a29fe7bd717c5a1d5f863054e8f260225fc7e0ad5f',
        'User-Agent': 'foo'
      },
      form: {
        portalId: req.body.id
      }
    }),
    // eslint-disable-next-line max-statements
    (err, response, body) => {
      if (err || response.statusCode >= 300) {
        console.log('error', err)
        if (response) {
          console.log(response.statusCode, body)
        }
        res.clearCookie('camacSession')
        res.clearCookie('portalId')
      } else {
        try {
          const json = JSON.parse(body)
          res.cookie('camacSession', json.hash)
          res.cookie('portalId', req.body.id)
          res.clearCookie('camacData')
        } catch (e) {
          // do nothing
        }
      }
      res.redirect(base)
    }
  )
})

function getOverview(session) {
  return new Promise((resolve, reject) => {
    request.post(
      authenticate({
        url: `${camacApi}/portal/user/overview/resource-id/248`,
        headers: {
          'X-Camac-Session': session,
          'User-Agent': 'foo'
        }
      }),
      (err, response, body) => {
        if (err || response.statusCode >= 300) {
          console.log('error', err, response.statusCode, body)
          reject()
        } else {
          try {
            const json = JSON.parse(body)
            resolve(json)
          } catch (e) {
            reject()
          }
        }
      }
    )
  })
}

app.get('/logout', (req, res) => {
  res.clearCookie('camacSession')
  res.clearCookie('portalId')
  res.clearCookie('camacData')
  res.redirect(base)
})

app.listen(PORT, () => {
  console.log(`I-Web-Portal-Mock listening on localhost:${PORT}`)
})
