export default function(server) {
  let forms = server.createList('form', 10)

  server.create('instance', { form: forms[0] })
  server.create('instance', { form: forms[1] })
  server.create('instance', { form: forms[2] })
  server.create('instance', { form: forms[3] })
  server.create('instance', { form: forms[4] })
}
