#!/usr/bin/env bats

export MOCK=1

@test "Show event" {
	run pontoon event show 999
	[ "$status" = 0 ]
	[ "${lines[0]}" = "Event 999" ]
}
