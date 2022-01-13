import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";

import config from "caluma-portal/config/environment";
import getPersonals from "caluma-portal/gql/queries/get-personals.graphql";

function findAnswerByRegex(answers, regexp) {
  const re = new RegExp(regexp);

  return answers.find((answer) => re.test(answer.question.slug))?.value;
}

function preparePerson(document) {
  const answers = document.answers.edges.map(({ node }) => node);

  return {
    firstName: findAnswerByRegex(
      answers,
      config.APPLICATION.personalSuggestions.firstNameRegexp
    ),
    lastName: findAnswerByRegex(
      answers,
      config.APPLICATION.personalSuggestions.lastNameRegexp
    ),
    juristicName: findAnswerByRegex(
      answers,
      config.APPLICATION.personalSuggestions.juristicNameRegexp
    ),
    email: findAnswerByRegex(
      answers,
      config.APPLICATION.personalSuggestions.emailRegexp
    ),
  };
}

export default class PersonalSuggestionsComponent extends Component {
  @queryManager apollo;

  suggestions = useTask(this, this.fetchSuggestions, () => [
    this.args.instanceId,
  ]);

  @dropTask
  *fetchSuggestions() {
    const response = yield this.apollo.query(
      {
        query: getPersonals,
        fetchPolicy: "network-only",
        variables: {
          instanceId: this.args.instanceId,
          tableQuestions: config.APPLICATION.personalSuggestions.tableQuestions,
        },
      },
      "allCases.edges"
    );

    return (response[0]?.node.document.answers.edges ?? []).map(
      ({ node: table }) => {
        return {
          label: table.question.label,
          suggestions: table.value.map(preparePerson),
        };
      }
    );
  }
}
