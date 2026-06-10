defmodule Ebau.Policies.Checks.HasActiveInstanceACL do
  @moduledoc """
  Filter check that authorizes when the actor has an active instance ACL
  reachable through the given relationship path.

  The `:via` option names the relationship steps from the current resource to
  a `Caluma.Workflow.Case`. The check then traverses `case.instance.active_instance_acls`
  and matches against the actor's user id, role id, service id, or service group id (any match authorizes).

  ## Examples

  Direct (resource is the case):

      policy action_type(:read) do
        authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: []}
      end

  Through a single relationship:

      policy action_type(:read) do
        authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: [:case]}
      end

  Multi-hop (e.g. row document → root document via `family`):

      policy action_type(:read) do
        authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: [:family, :case]}
      end
  """

  use Ash.Policy.FilterCheck

  @impl true
  def describe(opts) do
    "actor has an active instance ACL via #{Enum.join(full_path(opts), ".")}"
  end

  @impl true
  def filter(_actor, _context, opts) do
    path = full_path(opts)

    has_user_acl = expr(exists(^path, user_id == ^actor([:user, :id])))
    has_role_acl = expr(exists(^path, role_id == ^actor([:role, :id])))
    has_service_acl = expr(exists(^path, service_id == ^actor([:service, :id])))
    has_service_group_acl = expr(exists(^path, service_group_id == ^actor([:service_group, :id])))

    expr(^has_user_acl or ^has_role_acl or ^has_service_acl or ^has_service_group_acl)
  end

  defp full_path(opts), do: (opts[:via] || []) ++ [:instance, :active_instance_acls]
end
