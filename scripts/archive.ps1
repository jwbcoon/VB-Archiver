$py = Get-Command python
$archiver = $(split-path -parent $MyInvocation.MyCommand.Definition) + $(Write-Output "\archiver.py")

Start-Process $py $archiver