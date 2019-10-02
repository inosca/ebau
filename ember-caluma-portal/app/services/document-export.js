import { warn, assert } from "@ember/debug";
import Service, { inject as service } from "@ember/service";

const PEOPLE_SOURCES = {
  "personalien-gesuchstellerin": {
    familyName: "name-gesuchstellerin",
    givenName: "vorname-gesuchstellerin"
  },
  "personalien-vertreterin-mit-vollmacht": {
    familyName: "name-vertreterin",
    givenName: "vorname-vertreterin"
  },
  "personalien-grundeigentumerin": {
    familyName: "name-grundeigentuemerin",
    givenName: "vorname-grundeigentuemerin"
  },
  "personalien-gebaudeeigentumerin": {
    familyName: "name-gebaeudeeigentuemerin",
    givenName: "vorname-gebaeudeeigentuemerin"
  },
  "personalien-projektverfasserin": {
    familyName: "name-projektverfasserin",
    givenName: "vorname-projektverfasserin"
  }
};

const PEOPLE_TARGET = "8-freigabequittung";

export default Service.extend({
  intl: service(),
  fetch: service(),
  calumaStore: service(),

  /**
   * Fake an additional document for the PDF
   * where applicants can put their signatures.
   *
   * @param {Object} data The parsed document data to amend.
   * @method _prepareReceiptPage
   * @private
   */
  _prepareReceiptPage(data) {
    try {
      const sources = data.sections
        .find(section => section.slug === "1-allgemeine-informationen")
        .children.find(section => section.slug === "personalien")
        .children.filter(section =>
          Object.keys(PEOPLE_SOURCES).includes(section.slug)
        );

      const target = data.sections.find(
        section => section.slug === PEOPLE_TARGET
      );

      Object.assign(target, {
        slug: "8-unterschriften",
        label: `8. ${this.intl.t("pdf.signatures")}`,
        children: sources.map(table => ({
          type: "SignatureQuestion",
          label: table.label
            .replace(new RegExp(`^${this.intl.t("pdf.personalities")} -`), "")
            .trim(),
          people: table.rows.map(row => ({
            familyName: row.find(
              column => column.slug === PEOPLE_SOURCES[table.slug].familyName
            ).value,
            givenName: row.find(
              column => column.slug === PEOPLE_SOURCES[table.slug].givenName
            ).value
          }))
        }))
      });
    } catch (error) {
      warn("Failed to prepare receipt page", {
        id: "be-download-pdf.receipt-page-failed"
      });
    }

    return data;
  },

  /**
   * Submits the data (as JSON) to a service and gets a PDF back.
   * @see https://github.com/adfinis-sygroup/document-merge-service/
   *
   * @param {String} instanceId The document's instance ID.
   * @param {Document} document The Caluma Document to export.
   * @param {Object} options Additional options for future-proofing.
   * @method merge
   */
  async merge(instanceId, document, options = {}) {
    const convert = options.convert || "pdf";
    const field = document.findField("formulardownload-pdf");
    const navigation = this.calumaStore.find(`Navigation:${document.pk}`);

    let data = {
      caseId: instanceId,
      caseType: document.rootForm.name,
      sections: parseDocument(document, navigation),
      signatureMetadata: this.intl.t("pdf.signatureMetadata"),
      signatureTitle: this.intl.t("pdf.signature")
    };

    if (document.findField("personalien")) {
      data = this._prepareReceiptPage(data);
    }

    const template = field.question.meta.template;

    assert("A template must be passed to the fields meta", template);

    const response = await this.fetch.fetch(
      `/document-merge-service/api/v1/template/${template}/merge/`,
      {
        mode: "cors",
        method: "POST",
        headers: {
          "content-type": "application/json; charset=utf-8",
          accept: "*/*"
        },
        body: JSON.stringify({ data, convert })
      }
    );

    if (response.ok) {
      return response.blob();
    } else {
      throw new Error(response.statusText || response.status);
    }
  }
});

function parseDocument(document, navigation) {
  const fieldsets = document.fieldsets;

  if (fieldsets.length === 1) {
    return [
      {
        type: "FormQuestion",
        hidden: false,
        slug: document.rootForm.slug,
        label: document.rootForm.label,
        children: [
          {
            type: "FormQuestion",
            hidden: false,
            slug: document.rootForm.slug,
            label: document.rootForm.label,
            children: fieldsets[0].fields.map(parseQuestion).filter(visible)
          }
        ]
      }
    ];
  }

  return navigation.items
    .filter(item => !item.parent)
    .map(parseNavigationItem)
    .filter(visible);
}

function parseNavigationItem(item) {
  return {
    type: "FormQuestion",
    hidden: !item.visible,
    slug: item.slug,
    label: item.label,
    children: [
      ...item.fieldset.fields.map(parseQuestion),
      ...item.children.map(parseNavigationItem)
    ].filter(visible)
  };
}

function visible(section) {
  return section && !section.hidden;
}

/**
 * This is the wrapper function that invokes the right parser function
 * for the type of the given field.
 *
 * @param {Field} field
 */
function parseQuestion(field) {
  switch (field.question.__typename) {
    case "FormQuestion":
      return null;

    case "TextQuestion":
    case "TextareaQuestion":
    case "IntegerQuestion":
    case "FloatQuestion":
    case "DateQuestion":
      return parseSimpleQuestion(field);

    case "ChoiceQuestion":
      return parseChoiceQuestion(field);

    case "DynamicChoiceQuestion":
      return parseChoiceQuestion(field, true);

    case "MultipleChoiceQuestion":
      return {
        ...parseMultipleChoiceQuestion(field),
        ...(field.question.slug === "einreichen-button" ? { hidden: true } : {})
      };

    case "DynamicMultipleChoiceQuestion":
      return parseMultipleChoiceQuestion(field, true);

    case "StaticQuestion":
      return parseStaticQuestion(field);

    case "TableQuestion":
      return parseTableQuestion(field);

    default:
      warn(field);
  }
}

function parseSimpleQuestion(field) {
  return {
    type: field.question.__typename,
    hidden: field.hidden,
    slug: field.question.slug,
    label: field.question.label,
    value: field.answer.value
  };
}

function parseStaticQuestion(field) {
  return {
    type: field.question.__typename,
    hidden: field.hidden,
    slug: field.question.slug,
    content: field.question.staticContent
  };
}

function parseTableQuestion(field) {
  return {
    type: field.question.__typename,
    hidden: field.hidden,
    slug: field.question.slug,
    label: field.question.label,
    columns: field.question.rowForm.questions.edges.map(edge => ({
      label: edge.node.label
    })),
    rows: (field.answer.value || []).map(doc =>
      doc.fields.map(field => parseQuestion(field))
    )
  };
}

function parseChoiceQuestion(field, flatten = false, limit = undefined) {
  const choices =
    field.question.__typename === "ChoiceQuestion"
      ? field.question.choiceOptions.edges
      : field.question.dynamicChoiceOptions.edges;

  const mapped = {
    type: flatten ? "TextQuestion" : "ChoiceQuestion",
    hidden: field.hidden,
    slug: field.question.slug,
    label: field.question.label
  };

  if (flatten) {
    mapped.value =
      choices
        .filter(edge => edge.node.slug === field.answer.value)
        .map(edge => edge.node.label)
        .join(", ") || null;
  } else {
    mapped.choices = choices
      .map(choice => ({
        label: choice.node.label,
        checked: choice.node.slug === field.answer.value
      }))
      .slice(0, limit);
  }

  return mapped;
}

function parseMultipleChoiceQuestion(field, flatten = false, limit) {
  const choices =
    field.question.__typename === "MultipleChoiceQuestion"
      ? field.question.multipleChoiceOptions.edges
      : field.question.dynamicMultipleChoiceOptions.edges;

  const mapped = {
    type: flatten ? "TextQuestion" : "MultipleChoiceQuestion",
    hidden: field.hidden,
    slug: field.question.slug,
    label: field.question.label
  };

  if (flatten) {
    mapped.value =
      choices
        .filter(edge => field.answer.value.includes(edge.node.slug))
        .map(edge => edge.node.label)
        .join(", ") || null;
  } else {
    mapped.choices = choices
      .map(choice => ({
        label: choice.node.label,
        checked:
          Array.isArray(field.answer.value) &&
          field.answer.value.includes(choice.node.slug)
      }))
      .slice(0, limit);
  }

  return mapped;
}
