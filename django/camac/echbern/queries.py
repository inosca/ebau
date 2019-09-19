document_query = """\
query ($filter: [JSONValueFilterType]) {
  allDocuments(metaValue: $filter) {
    edges {
      node {
        id
        form {
          slug
          __typename
        }
        answers {
          edges {
            node {
              ...FieldAnswer
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment SimpleAnswer on Answer {
  id
  question {
    slug
    __typename
  }
  ... on StringAnswer {
    stringValue: value
    __typename
  }
  ... on IntegerAnswer {
    integerValue: value
    __typename
  }
  ... on FloatAnswer {
    floatValue: value
    __typename
  }
  ... on ListAnswer {
    listValue: value
    __typename
  }
  ... on FileAnswer {
    fileValue: value {
      uploadUrl
      downloadUrl
      metadata
      name
      __typename
    }
    __typename
  }
  ... on DateAnswer {
    dateValue: value
    __typename
  }
  __typename
}

fragment FieldAnswer on Answer {
  ...SimpleAnswer
  ... on TableAnswer {
    tableValue: value {
      id
      form {
        slug
        questions {
          edges {
            node {
              ...FieldQuestion
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      answers {
        edges {
          node {
            ...SimpleAnswer
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment SimpleQuestion on Question {
  slug
  label
  isRequired
  isHidden
  meta
  infoText
  ... on TextQuestion {
    textMaxLength: maxLength
    placeholder
    __typename
  }
  ... on TextareaQuestion {
    textareaMaxLength: maxLength
    placeholder
    __typename
  }
  ... on IntegerQuestion {
    integerMinValue: minValue
    integerMaxValue: maxValue
    placeholder
    __typename
  }
  ... on FloatQuestion {
    floatMinValue: minValue
    floatMaxValue: maxValue
    placeholder
    __typename
  }
  ... on ChoiceQuestion {
    choiceOptions: options {
      edges {
        node {
          slug
          label
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  ... on MultipleChoiceQuestion {
    multipleChoiceOptions: options {
      edges {
        node {
          slug
          label
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  ... on DynamicChoiceQuestion {
    dataSource
    dynamicChoiceOptions: options {
      edges {
        node {
          slug
          label
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  ... on DynamicMultipleChoiceQuestion {
    dataSource
    dynamicMultipleChoiceOptions: options {
      edges {
        node {
          slug
          label
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  ... on StaticQuestion {
    staticContent
    __typename
  }
  __typename
}

fragment FieldTableQuestion on Question {
  ... on TableQuestion {
    rowForm {
      slug
      questions {
        edges {
          node {
            ...SimpleQuestion
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment FieldQuestion on Question {
  ...SimpleQuestion
  ...FieldTableQuestion
  ... on FormQuestion {
    subForm {
      slug
      name
      questions {
        edges {
          node {
            ...SimpleQuestion
            ...FieldTableQuestion
            ... on FormQuestion {
              subForm {
                slug
                name
                questions {
                  edges {
                    node {
                      ...SimpleQuestion
                      ...FieldTableQuestion
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}\
"""
