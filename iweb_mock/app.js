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
		hash: req.cookies.camacSession
	})
})

app.post('/hash', (req, res) => {
	request.post({
		url: 'http://localhost:4300/portal/user/session/resource-id/245',
		headers: {
			'X-Auth': '123qwe',
			'User-Agent': 'foo'
		},
		form: {
			identifier: req.body.id
		}
	}, (err, httpResponse, body) => {
		if (err) {
			console.log('err', err)
			return
		}
		console.log('got response', body)
		try {
			const json = JSON.parse(body)
			res.cookie('camacSession', json.hash)
		} catch (e) {
			// do nothing
		}
		res.redirect('/')
	})
})

app.listen(PORT, () => {
	console.log(`I-Web-Portal-Mock listening on localhost:${PORT}`)
})
