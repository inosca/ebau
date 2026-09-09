defmodule Ebau.Mailer.ConfigTest do
  use ExUnit.Case, async: true

  alias Ebau.Mailer.Config

  describe "admins/1" do
    test "parses a comma separated list" do
      assert Config.admins("A Admin <a@example.com>,B Admin <b@example.com>") == [
               {"A Admin", "a@example.com"},
               {"B Admin", "b@example.com"}
             ]
    end

    test "trims the whitespace django leaves in the name" do
      assert Config.admins("A Admin <a@example.com>, B Admin <b@example.com>") == [
               {"A Admin", "a@example.com"},
               {"B Admin", "b@example.com"}
             ]
    end

    test "is empty without admins" do
      assert Config.admins("") == []
    end

    test "raises on a malformed entry, like django's parse_admins" do
      assert_raise RuntimeError, ~r/is not in the correct format/, fn ->
        Config.admins("a@example.com")
      end
    end
  end
end
