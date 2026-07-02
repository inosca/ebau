.PHONY: test
test-all:
	mix test
	@APPLICATION=kt_so mix test.so
	@APPLICATION=kt_gr mix test.gr

.PHONY: setup-test
setup-test:
	@cd .. && docker compose exec -e MIX_ENV=test elixir mix ebau.bootstrap_legacy_schema

