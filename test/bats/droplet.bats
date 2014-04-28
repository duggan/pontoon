#!/usr/bin/env bats

export MOCK=1

@test "List Droplets" {
	run pontoon droplet list
	[ "$status" = 0 ]
	[ "${lines[0]}" = "foo:            (2GB, Foobuntu 12.04 x64, Bardam 1, 192.0.2.1, active)" ]
}

@test "Detailed Droplet list" {
	run pontoon droplet list --detail
	[ "$status" = 0 ]
	[ "${lines[0]}" = "foo" ]
}

@test "Fail trying to create Droplet with existing hostname" {
	run pontoon droplet create foo
	[ "$status" = 1 ]
}

@test "Create a Droplet" {
	run pontoon droplet create something-different \
	--size="512MB" \
	--image="Foobuntu 12.04 x64" \
	--region="Bardam 1" \
	--no-wait # we should test the 'wait' variant too
	[ "$status" = 0 ]
}

@test "SSH into a Droplet" {
	skip "can't test SSH yet"
	run pontoon ssh foo
	[ "$status" = 0 ]
}

@test "Rename a Droplet" {
	run pontoon droplet rename foo new-foo
	[ "$status" = 0 ]
}

@test "Fail to rename a Droplet to an existing hostname" {
	run pontoon droplet rename foo bar
	[ "$status" = 1 ]
}

@test "Resize a Droplet" {
	run pontoon droplet resize foo 1gb
	[ "$status" = 0 ]
}

@test "Create a Droplet snapshot" {
	run pontoon droplet snapshot foo foo-snapshot-daily
	[ "$status" = 0 ]
}

@test "Show details for one Droplet" {
	run pontoon droplet show foo
	[ "$status" = 0 ]
	[ "${lines[0]}" = "foo" ]
}

@test "Show status for one Droplet" {
	run pontoon droplet status foo
	[ "$status" = 0 ]
	[ "${lines[0]}" = "active" ]
}

@test "Destroy a Droplet, scrub its data" {
	run pontoon droplet destroy foo
	[ "$status" = 0 ]
	[ "${lines[0]}" = "Destroying foo and scrubbing data..." ]
}

@test "Destroy a Droplet, don't scrub data" {
	run pontoon droplet destroy foo --no-scrub
	[ "$status" = 0 ]
	[ "${lines[0]}" = "Destroying foo..." ]
}

@test "Start a Droplet" {
	run pontoon droplet start foo
	[ "$status" = 0 ]
}

@test "Shutdown a Droplet" {
	run pontoon droplet shutdown foo
	[ "$status" = 0 ]
}

@test "Reboot a Droplet" {
	run pontoon droplet reboot foo
	[ "$status" = 0 ]
}

@test "Restore a Droplet from snapshot" {
	run pontoon droplet restore foo snapshot-foo
	[ "$status" = 0 ]
}

@test "Rebuild a Droplet using a default image" {
	run pontoon droplet rebuild foo "Foobuntu 12.04 x64"
	[ "$status" = 0 ]
}

@test "Powercycling a Droplet should create a warning" {
	skip "this really needs an expect script"
	run sh -c 'yes | pontoon droplet powercycle foo'
	[ "$status" = 0 ]
}

@test "Powercycling a Droplet, forced with --yes" {
	run pontoon droplet powercycle foo --yes
	[ "$status" = 0 ]
}

@test "Powering off a Droplet should create a warning" {
	skip "this really needs an expect script"
	run sh -c 'yes | pontoon droplet poweroff foo'
	[ "$status" = 0 ]
}

@test "Power a Droplet off, forced with --yes" {
	run pontoon droplet poweroff foo --yes
	[ "$status" = 0 ]
}

@test "Reset root password for a Droplet" {
	skip "this really needs an expect script"
	run sh -c 'yes | pontoon droplet passwordreset foo'
	[ "$status" = 0 ]
}

@test "Reset root password for a Droplet, forced with --yes" {
	run pontoon droplet passwordreset foo --yes
	[ "$status" = 0 ]
}

@test "Enable backups" {
	run pontoon droplet backups foo --enable
	[ "$status" = 0 ]
}

@test "Disable backups" {
	run pontoon droplet backups foo --disable
	[ "$status" = 0 ]
}

@test "Should be a single error message when incorrect arguments used" {
	run pontoon droplet backups foo
	[ "$output" = "action must be either 'enable' or 'disable'" ]
}

@test "'field' command expects 'field-name' argument" {
	run pontoon droplet field dev
	[ "$status" = 1 ]
}

@test "Provide output of a single field of a droplet's info" {
	run pontoon droplet field foo ip_address
	[ "$status" = 0 ]
}
