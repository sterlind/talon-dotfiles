param(
    [Parameter(Mandatory=$true, Position=0)][string] $Path
)

$file = Get-Item $Path
$file.LastWriteTime = (Get-Date)