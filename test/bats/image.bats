#!/usr/bin/env bats

export MOCK=1

@test "List images" {
	run pontoon image list
	[ "$status" = 0 ]
	[ "${lines[1]}" = " - Foobuntu 12.04 x64" ]
}

@test "List OSes" {
	run pontoon image oses
	[ "$status" = 0 ]
	[ "${lines[2]}" = " - Foobuntu" ]
}

@test "Show image details" {
	run pontoon image show "Foobuntu 12.04 x64"
	[ "$status" = 0 ]
	[ "${lines[0]}" = "   distribution: Foobuntu" ]
}
