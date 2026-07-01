defmodule Caluma.Form.Resolver do
  @moduledoc """
  Behaviour for resolving a `{module, opts}` tuple to a Caluma value — a
  question slug in most cases, or a value map for the `mapping` option.

  ## When to use

  Most fields map to a single, fixed question slug. For those, pass a plain
  string (or a list of strings) and skip the resolver entirely:

      answer :name, :string, question_id: "nachname"

  Reach for a resolver when the value is fixed per deployment but not known
  when you write the DSL — e.g. different cantons use different question slugs
  for the same logical field:

      answer :name, :string,
        question_id: {Ebau.Caluma.TenantResolver, %{default: "nachname", gr: "familienname"}}

  ## Where `resolve/1` is called

  The same `resolve(opts)` callback is invoked from three sites, at different
  times:

  - `question_id: {mod, opts}` — **compile time**, in
    `Caluma.Form.Extensions.Document.AnswerTransformer` (via
    `Caluma.Form.AnswerFilters`). The result is baked into the resource's
    relationship filter. Returns a slug string or list of strings.
  - `key: {mod, opts}` on `Caluma.Workflow.Calculations.CaseMeta` — **query
    time**, from `expression/2`. Returns a meta-key string.
  - `mapping: {mod, opts}` on `mapped_answer`/`mapped_list_answer` — **query
    time**, via `Caluma.Form.Calculations.DocumentAnswer.resolve_mapping/1`.

  In all three, `resolve/1` receives only `opts`; no query context is passed.

  ## Example: tenant-based resolver

      defmodule Ebau.Caluma.TenantResolver do
        @behaviour Caluma.Form.Resolver

        @tenant Application.compile_env(:ebau, :tenant)

        @impl true
        def resolve(mapping) do
          mapping[@tenant] || mapping[:default]
        end
      end

  The lookup is indifferent to *when* it runs: `mapping[@tenant]` is a slug
  string in the `question_id`/`key` cases and a value map in the `mapping`
  case. See `Ebau.Caluma.TenantResolver` for the real implementation.
  """

  @doc """
  Resolves a `{module, opts}` tuple to a Caluma value from `opts` alone (no
  query context).

  Returns a question slug string or list of strings for the `question_id`/`key`
  uses, or the value map for the `mapping` use. See the module docs for where
  each is invoked, and why a resolver must depend only on build-stable state.
  """
  @callback resolve(opts :: term()) ::
              String.t() | [String.t()] | %{optional(String.t()) => term()}
end
