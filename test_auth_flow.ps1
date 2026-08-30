# Test Authentication Flow
# This script tests the complete OTP authentication flow locally

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "IntelligentInsightAnalyzer - Authentication Flow Test" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

$API_URL = "http://localhost:9000"
$API_TIMEOUT = 10
$TEST_EMAIL = "test@example.com"

# Test 1: Health Check
Write-Host "[1/5] Testing backend health..." -ForegroundColor Yellow
$response = Invoke-WebRequest -Uri "$API_URL/health" -Method GET -UseBasicParsing
if ($response.StatusCode -eq 200) {
    Write-Host "✅ Backend is healthy" -ForegroundColor Green
} else {
    Write-Host "❌ Backend health check failed" -ForegroundColor Red
    exit 1
}

# Test 2: Send OTP
Write-Host "`n[2/5] Sending OTP to $TEST_EMAIL..." -ForegroundColor Yellow
$body = @{
    email = $TEST_EMAIL
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "$API_URL/auth/send-otp" -Method POST -ContentType "application/json" -Body $body -UseBasicParsing
$data = $response.Content | ConvertFrom-Json

if ($data.success) {
    Write-Host "✅ OTP sent successfully" -ForegroundColor Green
    Write-Host "   Message: $($data.message)" -ForegroundColor Gray
} else {
    Write-Host "❌ Failed to send OTP" -ForegroundColor Red
    exit 1
}

# Test 3: Extract OTP from logs (mock mode)
Write-Host "`n[3/5] Extracting OTP from backend..." -ForegroundColor Yellow
Write-Host "   (In mock mode, OTP is printed to backend console)" -ForegroundColor Gray
$OTP = "000000"  # Default for testing - user should check backend logs
Write-Host "   ⚠️  Manual step: Check backend logs for OTP code" -ForegroundColor Yellow
Write-Host "   ⚠️  Enter OTP code when prompted" -ForegroundColor Yellow

# Test 4: Verify OTP (with user input)
Write-Host "`n[4/5] Verifying OTP..." -ForegroundColor Yellow
$userOTP = Read-Host "Enter the OTP code from backend logs (6 digits)"

$body = @{
    email = $TEST_EMAIL
    otp = $userOTP
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "$API_URL/auth/verify-otp" -Method POST -ContentType "application/json" -Body $body -UseBasicParsing
$data = $response.Content | ConvertFrom-Json

if ($data.success) {
    Write-Host "✅ OTP verified successfully" -ForegroundColor Green
    Write-Host "   Email: $($data.email)" -ForegroundColor Gray
    
    $SESSION_TOKEN = $data.session_token
    Write-Host "   Session Token: $($SESSION_TOKEN.Substring(0, 8))..." -ForegroundColor Gray
} else {
    Write-Host "❌ OTP verification failed" -ForegroundColor Red
    Write-Host "   Error: $($data.message)" -ForegroundColor Red
    exit 1
}

# Test 5: Verify Session
Write-Host "`n[5/5] Verifying session..." -ForegroundColor Yellow
$body = @{
    session_token = $SESSION_TOKEN
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "$API_URL/auth/verify-session" -Method POST -ContentType "application/json" -Body $body -UseBasicParsing
$data = $response.Content | ConvertFrom-Json

if ($data.success) {
    Write-Host "✅ Session verified successfully" -ForegroundColor Green
    Write-Host "   Authenticated Email: $($data.email)" -ForegroundColor Gray
} else {
    Write-Host "❌ Session verification failed" -ForegroundColor Red
    exit 1
}

# Summary
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "✅ All tests passed!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "`n📋 Test Summary:" -ForegroundColor Cyan
Write-Host "  ✅ Backend health check" -ForegroundColor Green
Write-Host "  ✅ OTP generation and sending" -ForegroundColor Green
Write-Host "  ✅ OTP verification" -ForegroundColor Green
Write-Host "  ✅ Session creation" -ForegroundColor Green
Write-Host "  ✅ Session verification" -ForegroundColor Green
Write-Host "`n🚀 Authentication system is working correctly!" -ForegroundColor Green
Write-Host "`n📍 Access the frontend at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "   Backend API at: $API_URL" -ForegroundColor Cyan
