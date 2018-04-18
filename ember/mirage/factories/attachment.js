import { Factory } from 'ember-cli-mirage'

export default Factory.extend({
  afterCreate(attachment) {
    attachment.update({
      path: `/api/v1/attachments/${attachment.id}/files/${attachment.name}.png`
    })
  }
})
