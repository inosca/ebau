const express = require('express')
const exphbs = require('express-handlebars')
const request = require('request')
const cookieParser = require('cookie-parser')
const bodyParser = require('body-parser')

const PORT = 4400
const app = express()

app.use(cookieParser())
app.use(bodyParser())

app.engine('.hbs', exphbs({ defaultLayout: 'main', extname: '.hbs' }))
app.set('view engine', '.hbs')

app.get('/', (req, res) => {
	res.render('home', {
		hash: req.cookies.camacSession,
		id: req.cookies.portalId,
		overview: req.cookies.camacData
	})
})

app.post('/hash', (req, res) => {
	request.post({
		url: 'http://localhost:4300/portal/user/session/resource-id/245',
		headers: {
			'X-Auth': '340acc71664cde7b4b6608a29fe7bd717c5a1d5f863054e8f260225fc7e0ad5f',
			'User-Agent': 'foo'
		},
		form: {
			identifier: req.body.id
		}
	}, (err, response, body) => {
		if (err || response.statusCode >= 300) {
			console.log('error', err, response.statusCode, body)
			res.clearCookie('camacSession')
			res.clearCookie('portalId')
		} else {
			try {
				const json = JSON.parse(body)
				console.log('got session hash', json.hash)
				res.cookie('camacSession', json.hash)
				res.cookie('portalId', req.body.id)
				res.clearCookie('camacData')
			} catch (e) {
				// do nothing
			}
		}
		res.redirect('/')
	})
})

app.post('/overview', (req, res) => {
	request.post({
		url: 'http://localhost:4300/portal/user/overview/resource-id/245',
		headers: {
			'X-Camac-Session': req.cookies.camacSession,
			'User-Agent': 'foo'
		}
	}, (err, response, body) => {
		if (err || response.statusCode >= 300) {
			console.log('error', err, response.statusCode, body)
			res.clearCookie('camacSession')
			res.clearCookie('portalId')
			res.clearCookie('camacData')
		} else {
			try {
				const json = JSON.parse(body)
				res.cookie('camacData', json)
			} catch (e) {
				// do nothing
			}
		}
		res.redirect('/')
	})
})

app.listen(PORT, () => {
	console.log(`I-Web-Portal-Mock listening on localhost:${PORT}`)
})
