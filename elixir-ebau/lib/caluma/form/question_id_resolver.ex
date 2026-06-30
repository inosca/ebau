defmodule Caluma.Form.QuestionIdResolver do
  @moduledoc """
  Behaviour for dynamically resolving Caluma question IDs at query time.

  ## When to use

  Most fields map to a single, fixed question slug. For those, pass a plain
  string as the `question_id` in the `caluma_document` DSL:

      answer :name, :string, question_id: "nachname"

  A resolver is needed when the question slug isn't known at compile time —
  for example, when different tenants, cantons, or environments use different
  Caluma forms with different question slugs for the same logical field.

  ## How it works

  1. In the `caluma_document` DSL, pass a `{module, opts}` tuple:

         answer :name, :string,
           question_id: {MyApp.TenantResolver, %{default: "nachname", tenant_a: "full-name"}}

  2. At query time, `Caluma.Form.Calculations.DocumentAnswer` calls
     `module.resolve(opts, context)` where:

     - `opts` is whatever you passed as the second element of the tuple
       (a map, a keyword list, a string — anything you need)
     - `context` is the Ash calculation context, which includes the actor
       and any custom context set via `Ash.Context.set/2`

  3. Your `resolve/2` must return either:

     - A single question ID string — generates `WHERE question_id = 'slug'`
     - A list of strings — generates `WHERE question_id IN ('a', 'b')`

  ## Example: tenant-based resolver

      defmodule MyApp.TenantResolver do
        @behaviour Caluma.Form.QuestionIdResolver

        @impl true
        def resolve(mapping, context) do
          tenant = context[:tenant]
          mapping[tenant] || mapping[:default]
        end
      end

  ## Example: environment-based resolver

      defmodule MyApp.EnvResolver do
        @behaviour Caluma.Form.QuestionIdResolver

        @impl true
        def resolve(mapping, _context) do
          env = Application.get_env(:my_app, :environment)
          mapping[env] || mapping[:default]
        end
      end

  In the ebau project, `Ebau.Caluma.CantonResolver` is a real-world
  implementation that resolves question IDs based on the current canton
  from the Ash context.
  """

  @doc """
  Resolves a question ID (or list of IDs) from the given opts and context.

  Called at query time by `Caluma.Form.Calculations.DocumentAnswer`. Must
  return either a single question ID string or a list of question ID strings.
  """
  @callback resolve(opts :: term()) :: String.t() | [String.t()]
end
