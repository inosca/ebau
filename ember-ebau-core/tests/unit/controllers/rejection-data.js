import { default as id } from "dummy/tests/helpers/graphql-id";

export const DISTRIBUTION_EMPTY = {
  distribution: {
    totalCount: 0,
    __typename: "WorkItemConnection",
  },
};

export const DISTRIBUTION_NOT_EMPTY = {
  distribution: {
    totalCount: 1,
    __typename: "WorkItemConnection",
  },
};

export const CLAIMS_EMPTY = {
  claims: {
    edges: [
      {
        node: {
          id: id("Case"),
          workItems: {
            edges: [
              {
                node: {
                  id: id("WorkItem"),
                  document: {
                    id: id("Document"),
                    answers: {
                      edges: [
                        {
                          node: {
                            id: id("TableAnswer"),
                            value: [
                              {
                                id: id("Document"),
                                answers: {
                                  edges: [
                                    {
                                      node: {
                                        id: id("StringAnswer"),
                                        value:
                                          "nfd-tabelle-status-abgeschlossen",
                                        __typename: "StringAnswer",
                                      },
                                      __typename: "AnswerEdge",
                                    },
                                  ],
                                  __typename: "AnswerConnection",
                                },
                                __typename: "Document",
                              },
                            ],
                            __typename: "TableAnswer",
                          },
                          __typename: "AnswerEdge",
                        },
                      ],
                      __typename: "AnswerConnection",
                    },
                    __typename: "Document",
                  },
                  __typename: "WorkItem",
                },
                __typename: "WorkItemEdge",
              },
            ],
            __typename: "WorkItemConnection",
          },
          __typename: "Case",
        },
        __typename: "CaseEdge",
      },
    ],
    __typename: "CaseConnection",
  },
};

export const CLAIMS_NOT_EMPTY = {
  claims: {
    edges: [
      {
        node: {
          id: id("Case"),
          workItems: {
            edges: [
              {
                node: {
                  id: id("WorkItem"),
                  document: {
                    id: id("Document"),
                    answers: {
                      edges: [
                        {
                          node: {
                            id: id("TableAnswer"),
                            value: [
                              {
                                id: id("Document"),
                                answers: {
                                  edges: [
                                    {
                                      node: {
                                        id: id("StringAnswer"),
                                        value:
                                          "nfd-tabelle-status-in-bearbeitung",
                                        __typename: "StringAnswer",
                                      },
                                      __typename: "AnswerEdge",
                                    },
                                  ],
                                  __typename: "AnswerConnection",
                                },
                                __typename: "Document",
                              },
                            ],
                            __typename: "TableAnswer",
                          },
                          __typename: "AnswerEdge",
                        },
                      ],
                      __typename: "AnswerConnection",
                    },
                    __typename: "Document",
                  },
                  __typename: "WorkItem",
                },
                __typename: "WorkItemEdge",
              },
            ],
            __typename: "WorkItemConnection",
          },
          __typename: "Case",
        },
        __typename: "CaseEdge",
      },
    ],
    __typename: "CaseConnection",
  },
};
