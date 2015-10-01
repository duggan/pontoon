#!/usr/bin/env bats

@test "PEP8 tests for interface code" {
	skip "Moved to tox"
	run pep8 scripts/pontoon*
	[ "$status" = 0 ]
}
