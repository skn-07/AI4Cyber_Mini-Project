$PythonScript = "C:\AI4Cyber\FinalSubmission\scriptAnalyzer.py"
$CondaPython = "C:\Users\DragonzVM\miniconda3\envs\AI4Cyber\python.exe"  # Update with the actual path

while ($true) {
    # Display the current working directory to simulate a PowerShell prompt
    $CurrentDir = Get-Location
    Write-Host "PS {Malicious Analyzer} $CurrentDir> " -NoNewline

    # Read the input command
    $Command = Read-Host

    # Run the Python script in the Conda environment and pass the command directly as an argument
    $Result = & $CondaPython $PythonScript "$Command"

    # Parse the Python script's output (prediction and probabilities)
    $OutputLines = $Result -split "`n"
    $Prediction = $OutputLines[0].Trim()
    $MalProb = $OutputLines[1].Trim()
    $BenProb = $OutputLines[2].Trim()

    # Display the result
    if ($Prediction -eq "1") {
        Write-Host "The script is classified as Malicious." -ForegroundColor Red
        Write-Host "Probability of Malicious: $MalProb" -ForegroundColor Cyan
        Write-Host "Probability of Benign: $BenProb" -ForegroundColor Cyan
    } elseif ($Prediction -eq "0") {
        Write-Host "The script is classified as Benign." -ForegroundColor Green
        Write-Host "Probability of Benign: $BenProb" -ForegroundColor Cyan
        Write-Host "Probability of Malicious: $MalProb" -ForegroundColor Cyan
    } else {
        Write-Host "Unable to determine script classification. Please check the Python script." -ForegroundColor Yellow
        continue
    }

    # Ask the user whether to execute the script
    $Execute = Read-Host "Do you want to execute the script? (yes/no)"
    if ($Execute -eq "yes") {
        # Execute the PowerShell command
        try {
            Invoke-Expression $Command
        } catch {
            Write-Host "Error executing the script: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "The script execution was canceled." -ForegroundColor Yellow
    }
}
