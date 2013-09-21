#!/usr/bin/env bats

export MOCK=1

@test "List sizes" {
	run pontoon size list
	[ "$status" = 0 ]
	[ "${lines[1]}" = " - 512MB" ]
	[ "${lines[2]}" = " - 1GB" ]
}
