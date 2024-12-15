# Démarrage des services FastAPI
Write-Host "Starting embedding service on port 8001..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "app\embedding_service.py"

Write-Host "Starting database service on port 8002..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "app\db_service.py"

Write-Host "Starting composite service on port 8000..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "app\composite_service.py"

# Démarrage du file watcher
Write-Host "Starting file watcher..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "watcher\file_watcher.py"

# Attendre quelques secondes pour s'assurer que les services sont en ligne
Write-Host "Waiting for services to start..."
Start-Sleep -Seconds 5

# Vérification des services (optionnel)
Write-Host "Checking if services are online..."
try {
    Invoke-WebRequest -Uri "http://localhost:8000/docs" -UseBasicParsing | Out-Null
    Invoke-WebRequest -Uri "http://localhost:8001/docs" -UseBasicParsing | Out-Null
    Invoke-WebRequest -Uri "http://localhost:8002/docs" -UseBasicParsing | Out-Null
    Write-Host "All services are online."
} catch {
    Write-Host "Error: One or more services are not responding."
    Exit
}

# Démarrage de l'interface graphique
Write-Host "Starting graphical interface..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "interface.py"
