import CamacInputComponent from 'citizen-portal/components/camac-input/component'
import { computed } from '@ember/object'
import { reads } from '@ember/object/computed'
import { inject as service } from '@ember/service'
import { task } from 'ember-concurrency'
import UIkit from 'uikit'
import fetch from 'fetch'
import Ember from 'ember'
import download from 'downloadjs'
import computedTask from 'citizen-portal/lib/computed-task'

const { testing } = Ember

const allowedMimeTypes = ['application/pdf', 'image/png', 'image/jpeg']

export default CamacInputComponent.extend({
  ajax: service(),
  store: service(),
  session: service(),

  token: reads('session.data.authenticated.access_token'),

  headers: computed('token', function() {
    return {
      Authorization: `Bearer ${this.get('token')}`
    }
  }),

  classNameBindings: ['hidden.lastSuccessful.value:uk-hidden'],
  classNames: ['uk-margin-remove', 'uk-animation-fade'],

  mimeTypes: allowedMimeTypes.join(','),

  hidden: computedTask('_hidden', 'question.hidden'),
  _hidden: task(function*() {
    return yield (yield this.get('question')).get('hidden')
  }),

  download: task(function*() {
    try {
      let question = yield this.get('question')

      if (!question.get('model.path')) {
        return
      }

      let response = yield fetch(question.get('model.path'), {
        mode: 'cors',
        headers: this.get('headers')
      })

      let file = yield response.blob()

      if (!testing) {
        download(file, question.get('model.name'), file.type)
      }

      UIkit.notification('Datei wurde erfolgreich heruntergeladen', {
        status: 'success'
      })
    } catch (e) {
      UIkit.notification(
        'Hoppla, beim Herunterladen der Datei ist etwas schief gelaufen. Bitte versuchen Sie es nochmals',
        { status: 'danger' }
      )
    }
  }),

  upload: task(function*(files) {
    if (this.get('readonly')) {
      return
    }

    try {
      let file = files.item(0)

      if (!allowedMimeTypes.includes(file.type)) {
        UIkit.notification(
          'Es können nur PDF, JPEG oder PNG Dateien hochgeladen werden.',
          { status: 'danger' }
        )

        return
      }

      let question = yield this.get('question')

      let filename = `${question.get('name')}.${file.name.split('.').pop()}`

      let formData = new FormData()
      formData.append('instance', question.get('model.instance.id'))
      formData.append('path', file, filename)

      let response = yield this.get('ajax').request('/api/v1/attachments', {
        method: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        data: formData,
        headers: {
          Accept: 'application/vnd.api+json'
        }
      })

      this.get('store').pushPayload(response)

      question.set(
        'model',
        this.get('store').peekRecord('attachment', response.data.id)
      )

      UIkit.notification('Die Datei wurde erfolgreich hochgeladen', {
        status: 'success'
      })
    } catch (e) {
      UIkit.notification(
        'Hoppla, beim Hochladen der Datei ist etwas schief gelaufen. Bitte versuchen Sie es nochmals',
        { status: 'danger' }
      )
    }
  }),

  actions: {
    triggerUpload() {
      this.get('element')
        .querySelector('input[type=file')
        .click()
    }
  }
})
