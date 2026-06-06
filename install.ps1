param(
  [Parameter(Mandatory=$true)][string]$Target,
  [switch]$Overwrite
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetFull = (New-Item -ItemType Directory -Force -Path $Target).FullName
$Claude = Join-Path $TargetFull ".claude"
New-Item -ItemType Directory -Force -Path $Claude | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetFull "docs\ros2-quality") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetFull "docs\ros2-design") | Out-Null

function Copy-Dir($Name) {
  $Src = Join-Path $Root $Name
  $Dst = Join-Path $Claude $Name
  if (!(Test-Path $Src)) { return }
  if ((Test-Path $Dst) -and (-not $Overwrite)) {
    Write-Host "SKIP existing $Dst; use -Overwrite to replace"
    return
  }
  if (Test-Path $Dst) { Remove-Item -Recurse -Force $Dst }
  Copy-Item -Recurse -Force $Src $Dst
  Write-Host "installed .claude/$Name"
}

@("commands","skills","agents","references","subagent_templates","tools","hooks","evals","workspace_template","docs") | ForEach-Object { Copy-Dir $_ }

@"
# ROS2 Forge Skills Installed

Installed from: $Root
Installed to: $TargetFull

Start Claude Code in this workspace and run:

````text
/ros2
````
"@ | Set-Content -Encoding UTF8 (Join-Path $Claude "ROS2_FORGE_INSTALLED.md")

Write-Host "OK: ROS2 Forge Skills v4.2 installed into $Claude"
