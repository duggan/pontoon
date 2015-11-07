#!/usr/bin/env bats

export MOCK=1

@test "List SSH keys" {
	run pontoon sshkey list
	[ "$status" = 0 ]
	[ "${lines[1]}" = " - Example Key" ]
}

@test "Add SSH key" {
	skip "New lib checks syntax, need a workaround"
	run pontoon sshkey add foo `mktemp -t pontoontest.XXXXX`
	[ "$status" = 0 ]
}

@test "Show SSH key" {
	run pontoon sshkey show "Example Key"
	[ "$status" = 0 ]
}

@test "Fail to show non-existant key" {
	run pontoon sshkey show Nope
	[ "$status" = 1 ]
}

@test "Replace an existing key" {
	skip "New lib checks syntax, need a workaround"
	run pontoon sshkey replace "Example Key" `mktemp -t pontoontest.XXXXX`
	[ "$status" = 0 ]
}

@test "Fail to replace a non-existant key" {
	skip "New lib checks syntax, need a workaround"
	run pontoon sskey replace Nope `mktemp -t pontoontest.XXXXX`
	[ "$status" = 1 ]
}

@test "Destroy a key" {
	run pontoon sshkey destroy "Example Key"
	[ "$status" = 0 ]
}
