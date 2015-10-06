# Setup script for PyPI

function SetupPyPI ($server, $user, $pass) {
$config = @"
[pypi]
repository = https://$server.python.org/pypi
username = $user
password = $pass
"@
  $config | Out-File -FilePath $env:USERPROFILE\.pypirc -Encoding ASCII
}

function main () {
  Write-Host "Setting up PyPI..."
  SetupPyPI testpypi $env:test_user $env:test_pass
  Write-Host "PyPI configuration written."
}

main
