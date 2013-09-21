#!/usr/bin/env bats

export MOCK=1

@test "Show regions" {
	run pontoon region list
	[ "$status" = 0 ]
	[ "${lines[1]}" = " - Foo York 1" ]
}
