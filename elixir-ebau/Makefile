.PHONY: test-all
test-all:
	mix clean
	mix test
	mix clean
	@APPLICATION=kt_so mix test.so
	mix clean
	@APPLICATION=kt_gr mix test.gr
	mix clean
	@APPLICATION=kt_sg mix test.sg

.PHONY: setup-test
setup-test:
	@cd .. && docker compose up --build -d elixir && docker compose exec -e MIX_ENV=test elixir mix ebau.bootstrap_legacy_schema

.PHONY: makemessages
makemessages:
	@mix gettext.extract --merge
