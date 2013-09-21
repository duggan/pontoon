#!/usr/bin/env bats

@test "PEP8 tests for interface code" {
	run pep8 scripts/pontoon*
	[ "$status" = 0 ]
}
