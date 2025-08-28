# Configure-DoT.ps1
# Requires: Windows 11, PowerShell 5+ (Run as Administrator)
# PowerShell: Set-ExecutionPolicy Bypass -Scope Process -Force
# PowerShell: .\Configure-DoT.ps1

# 1. Ensure script is elevated
if (-not ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
    [Security.Principal.WindowsBuiltInRole]::Administrator)) {
  Write-Error "This script must be run as Administrator."
  exit 1
}

# 2. Enable DNS-over-TLS globally
Write-Host "Enabling DNS-over-TLS (DoT) globally…" -ForegroundColor Cyan
netsh dns add global dot=yes

# 3. Add DoT servers
$dotServers = @(
  @{ Server = "208.67.222.222"; DoTHost = "dns.umbrella.com" },
  @{ Server = "208.67.220.220"; DoTHost = "dns.umbrella.com" },
  @{ Server = "8.8.8.8"      ; DoTHost = "dns.google"     },
  @{ Server = "8.8.4.4"      ; DoTHost = "dns.google"     },
  @{ Server = "1.1.1.1"      ; DoTHost = "one.one.one.one"}
)

foreach ($entry in $dotServers) {
  Write-Host "Adding DoT server $($entry.Server) → $($entry.DoTHost)" -ForegroundColor Yellow
  netsh dns add encryption `
    server=$($entry.Server) `
    dothost=$($entry.DoTHost) `
    autoupgrade=yes
}

# 4. Flush DNS cache
Write-Host "Flushing DNS resolver cache…" -ForegroundColor Cyan
ipconfig /flushdns

# 5. Show current DoT/global settings
Write-Host "`n=== DNS-over-TLS & Global Settings ===" -ForegroundColor Green
netsh dns show global
netsh dns show encryption

# 6. Show full network config
Write-Host "`n=== Full Network Configuration ===" -ForegroundColor Green
ipconfig /all
