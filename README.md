$readmeContent = @"
---
title: Viwer3D
emoji: 🏗️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Viwer3D
Visualizador médico 3D utilizando Trame e VTK.
"@

[System.IO.File]::WriteAllText("$(Get-Location)\README.md", $readmeContent, (New-Object System.Text.UTF8Encoding($false)))