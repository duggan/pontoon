#!/usr/bin/env bats

export MOCK=1

@test "List snapshots" {
	run pontoon snapshot list
	[ "$status" = 0 ]
	[ "${lines[1]}" = " - snapshot-foo" ]
}

@test "Show snapshot details" {
	run pontoon snapshot show "snapshot-foo"
	[ "$status" = 0 ]
	[ "${lines[0]}" = "   distribution: Foobuntu" ]
	[ "${lines[1]}" = "   id: 1024" ]
	[ "${lines[2]}" = "   name: snapshot-foo" ]
}

@test "Destroy snapshot" {
	run pontoon snapshot destroy "snapshot-foo"
	[ "$status" = 0 ]
	[ "${lines[0]}" = "Destroying snapshot-foo..." ]
}

@test "Fail to destroy non-existant snapshot" {
	run pontoon snapshot destroy "snapshot-bar"
	[ "$status" = 1 ]
	[ "${lines[1]}" = 'No snapshot named "snapshot-bar" found' ]
}

@test "Transfer a snapshot" {
	run pontoon snapshot transfer "snapshot-foo" "Bardam 1"
	[ "$status" = 0 ]
}
