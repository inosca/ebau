defmodule Ebau.Legacy.ConfigLoader do
  @moduledoc """
  Loads selected legacy JSON fixture files into current database.

  This module is explicit fixture-loading layer for Elixir tests and setup tasks.
  It reads JSON files from configured legacy fixture root, defaulting to
  `../django/<application>/config` and `../django/<application>/data`,
  filters down to supported Django models, then bulk-inserts those rows into legacy and Caluma
  tables owned by Elixir app.

  Main use cases:

  - bootstrap selected canton/application config in tests
  - load real production-like Caluma forms and workflows for integration tests
  - support explicit `mix ebau.load_config` task

  This loader does **not** aim to be full replacement for Django `loaddata` or
  `camac_load.py`. It currently supports only subset of models needed by Elixir app.

  Typical usage:

      Ebau.Legacy.ConfigLoader.load_application_config!("kt_so")

      Ebau.Legacy.ConfigLoader.load_application_config!("kt_so", scope: :all)

      Ebau.Legacy.ConfigLoader.load_files!([
        "/abs/path/to/django/kt_so/config/user.json",
        "/abs/path/to/django/kt_so/config/caluma_workflow.json",
        "/abs/path/to/django/kt_so/config/caluma_form.json"
      ])

  Import order matters. Rows are inserted in dependency-safe order:

  1. `user.role`
  2. `user.servicegroup`
  3. `caluma_form.form`
  4. `caluma_form.question`
  5. `caluma_workflow.workflow`
  6. `caluma_form.formquestion`
  """

  alias Ebau.Repo

  @type application :: String.t()
  @type scope :: :config | :all
  @type fixture_path :: String.t()
  @type model :: String.t()

  @supported_models [
    "caluma_form.form",
    "caluma_form.question",
    "caluma_form.formquestion",
    "caluma_workflow.workflow",
    "user.role",
    "user.servicegroup"
  ]

  @doc """
  Loads fixture files for given Django application into current database.

  By default this loads `config/*.json`. Pass `scope: :all` to include
  `data/*.json`, and `include_init?: true` to append `init.json` when present.

  ## Examples

      iex> Ebau.Legacy.ConfigLoader.load_application_config!("kt_so")
      :ok

      iex> Ebau.Legacy.ConfigLoader.load_application_config!("kt_so", scope: :all)
      :ok
  """
  @spec load_application_config!(application(), keyword()) :: :ok
  def load_application_config!(application, opts \\ []) do
    scope = Keyword.get(opts, :scope, :config)
    include_init? = Keyword.get(opts, :include_init?, false)

    application
    |> application_files!(scope, include_init?)
    |> load_files!()
  end

  @doc """
  Returns fixture files for given Django application.

  `scope` controls whether only `config/*.json` or both `config/*.json` and
  `data/*.json` are returned. `include_init?` appends `init.json` when present.
  """
  @spec application_files!(application(), scope(), boolean()) :: [fixture_path()]
  def application_files!(application, scope \\ :config, include_init? \\ false) do
    application_dir = Path.join(django_root(), application)

    patterns =
      case scope do
        :config -> ["config/*.json"]
        :all -> ["config/*.json", "data/*.json"]
      end

    files =
      patterns
      |> Enum.flat_map(fn pattern ->
        application_dir
        |> Path.join(pattern)
        |> Path.wildcard()
      end)
      |> Enum.sort()

    files =
      if include_init? do
        init_path = Path.join(application_dir, "init.json")

        if File.exists?(init_path) do
          files ++ [init_path]
        else
          files
        end
      else
        files
      end

    if files == [] do
      raise ArgumentError,
            "no fixture files found for application #{inspect(application)} with scope #{inspect(scope)}"
    end

    files
  end

  @doc """
  Returns currently supported Django fixture model names.
  """
  @spec supported_models() :: [model()]
  def supported_models, do: @supported_models

  @doc """
  Loads explicit list of JSON fixture files.

  Files are decoded, filtered to supported models, then inserted into current database.

  ## Examples

      iex> Ebau.Legacy.ConfigLoader.load_files!([
      ...>   "/abs/path/to/django/kt_so/config/user.json",
      ...>   "/abs/path/to/django/kt_so/config/caluma_workflow.json"
      ...> ])
      :ok
  """
  @spec load_files!([fixture_path()]) :: :ok
  def load_files!(paths) do
    entries =
      paths
      |> Enum.flat_map(&read_entries!/1)
      |> Enum.filter(&(&1["model"] in @supported_models))

    Repo.transaction(fn ->
      groups = Enum.group_by(entries, & &1["model"])

      import_roles!(groups["user.role"] || [])
      import_service_groups!(groups["user.servicegroup"] || [])
      import_forms!(groups["caluma_form.form"] || [])
      import_questions!(groups["caluma_form.question"] || [])
      import_workflows!(groups["caluma_workflow.workflow"] || [])
      import_form_questions!(groups["caluma_form.formquestion"] || [])
    end)

    :ok
  end

  defp read_entries!(path) do
    path
    |> File.read!()
    |> JSON.decode!()
  end

  defp django_root do
    System.get_env("LEGACY_FIXTURE_ROOT") ||
      Application.get_env(:ebau, :legacy_fixture_root) ||
      default_django_root()
  end

  defp default_django_root do
    if Code.ensure_loaded?(Mix.Project) do
      Mix.Project.project_file()
      |> Path.dirname()
      |> Path.join("../django")
      |> Path.expand()
    else
      raise ArgumentError,
            "no LEGACY_FIXTURE_ROOT env var or :legacy_fixture_root config set, " <>
              "and Mix is not available in this environment"
    end
  end

  defp import_roles!(entries), do: bulk_upsert!("ROLE", entries, &role_row/1, [:ROLE_ID])

  defp import_service_groups!(entries),
    do: bulk_upsert!("SERVICE_GROUP", entries, &service_group_row/1, [:SERVICE_GROUP_ID])

  defp import_forms!(entries), do: bulk_upsert!("caluma_form_form", entries, &form_row/1, [:slug])

  defp import_questions!(entries),
    do: bulk_upsert!("caluma_form_question", entries, &question_row/1, [:slug])

  defp import_workflows!(entries),
    do: bulk_upsert!("caluma_workflow_workflow", entries, &workflow_row/1, [:slug])

  defp import_form_questions!(entries),
    do:
      bulk_upsert!("caluma_form_formquestion", entries, &form_question_row/1, [
        :form_id,
        :question_id
      ])

  defp bulk_upsert!(_table, [], _row_fn, _conflict_target), do: :ok

  defp bulk_upsert!(table, entries, row_fn, conflict_target) do
    Repo.insert_all(table, Enum.map(entries, row_fn),
      on_conflict: :nothing,
      conflict_target: conflict_target
    )

    :ok
  end

  defp role_row(%{"pk" => id, "fields" => fields}) do
    %{
      ROLE_ID: id,
      NAME: fields["name"],
      GROUP_PREFIX: fields["group_prefix"],
      slug: fields["slug"],
      ROLE_PARENT_ID: fields["role_parent"]
    }
  end

  defp service_group_row(%{"pk" => id, "fields" => fields}) do
    %{
      SERVICE_GROUP_ID: id,
      NAME: fields["name"],
      sort: fields["sort"],
      slug: fields["slug"]
    }
  end

  defp audit_fields(fields) do
    %{
      created_at: timestamp(fields["created_at"]),
      modified_at: timestamp(fields["modified_at"]),
      created_by_user: fields["created_by_user"],
      created_by_group: fields["created_by_group"],
      modified_by_user: fields["modified_by_user"],
      modified_by_group: fields["modified_by_group"]
    }
  end

  defp form_row(%{"pk" => slug, "fields" => fields}) do
    Map.merge(audit_fields(fields), %{
      slug: slug,
      name: json_map!(fields["name"]),
      description: json_map(fields["description"]),
      meta: fields["meta"] || %{},
      is_published: fields["is_published"] || false,
      is_archived: fields["is_archived"] || false,
      source_id: fields["source"]
    })
  end

  defp question_row(%{"pk" => slug, "fields" => fields}) do
    Map.merge(audit_fields(fields), %{
      slug: slug,
      label: json_map!(fields["label"]),
      type: fields["type"],
      # is_required and is_hidden are JEXL expression strings in Caluma, not booleans
      is_required: fields["is_required"] || "false",
      is_hidden: fields["is_hidden"] || "false",
      is_archived: fields["is_archived"] || false,
      configuration: fields["configuration"] || %{},
      meta: fields["meta"] || %{},
      row_form_id: fields["row_form"],
      sub_form_id: fields["sub_form"],
      source_id: fields["source"],
      info_text: json_map(fields["info_text"]),
      placeholder: json_map(fields["placeholder"]),
      data_source: fields["data_source"],
      static_content: json_map(fields["static_content"]),
      format_validators: json_list(fields["format_validators"]),
      default_answer_id: uuid(fields["default_answer"]),
      calc_dependents: json_list(fields["calc_dependents"]),
      calc_expression: fields["calc_expression"],
      hint_text: json_map(fields["hint_text"])
    })
  end

  defp workflow_row(%{"pk" => slug, "fields" => fields}) do
    Map.merge(audit_fields(fields), %{
      slug: slug,
      name: json_map!(fields["name"]),
      description: json_map(fields["description"]),
      meta: fields["meta"] || %{},
      is_published: fields["is_published"] || false,
      is_archived: fields["is_archived"] || false,
      allow_all_forms: fields["allow_all_forms"] || false
    })
  end

  defp form_question_row(%{"pk" => id, "fields" => fields}) do
    Map.merge(audit_fields(fields), %{
      id: id,
      sort: fields["sort"] || 0,
      form_id: fields["form"],
      question_id: fields["question"]
    })
  end

  defp timestamp(nil), do: nil

  defp timestamp(value) do
    case DateTime.from_iso8601(value) do
      {:ok, datetime, _offset} ->
        datetime

      {:error, reason} ->
        raise ArgumentError, "invalid timestamp #{inspect(value)}: #{inspect(reason)}"
    end
  end

  defp json_map(nil), do: nil
  defp json_map(value) when is_map(value), do: value
  defp json_map(value) when is_binary(value), do: JSON.decode!(value)

  defp json_map!(value) do
    case json_map(value) do
      nil -> raise ArgumentError, "expected JSON map, got nil"
      map -> map
    end
  end

  defp json_list(nil), do: []
  defp json_list(value) when is_list(value), do: value
  defp json_list(value) when is_binary(value), do: JSON.decode!(value)

  defp uuid(nil), do: nil
  defp uuid(value), do: Ecto.UUID.dump!(value)
end
