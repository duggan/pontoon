#!/usr/bin/env bats

export MOCK=1

@test "Show event" {
	run pontoon event show 54321
	[ "$status" = 0 ]
	[ "${lines[0]}" = "Event 54321" ]
}
