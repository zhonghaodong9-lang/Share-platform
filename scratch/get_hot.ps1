[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12

$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try {
    $resp = Invoke-RestMethod -Uri "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d92b410797300c730ed05b2d3513b&fltt=2&invt=2&fid=f6&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14,f2,f3,f6" -Headers $headers -TimeoutSec 5
    $idx = 1
    foreach ($item in $resp.data.diff) {
        Write-Host "No.$idx $($item.f14) ($($item.f12)) - 最新价: $($item.f2) - 涨跌: $($item.f3)%"
        $idx++
    }
} catch {
    Write-Host "请求失败: $_"
}
