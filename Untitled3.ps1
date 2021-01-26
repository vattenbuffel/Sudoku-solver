$Job = Start-Job -ScriptBlock {Write-Output 'Hello World'}
Receive-Job $Job