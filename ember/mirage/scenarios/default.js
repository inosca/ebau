export default function(server) {
  let forms = server.createList('form', 5)

  server.create('instance', { formId: forms[0].id })
  server.create('instance', { formId: forms[1].id })
  server.create('instance', { formId: forms[2].id })
  server.create('instance', { formId: forms[3].id })
  server.create('instance', { formId: forms[4].id })
}
