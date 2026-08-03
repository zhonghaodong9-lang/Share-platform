$jsonStr = curl.exe -k -s "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=5`&klt=101`&fields1=f1,f2,f3,f7`&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63`&secid=1.600487"
$obj = $jsonStr | ConvertFrom-Json

Write-Host "=== 亨通光电 (600487) 东方财富网页端直连权威数据 ==="
foreach ($line_str in $obj.data.klines) {
    $parts = $line_str.Split(",")
    $date = $parts[0]
    $main = [math]::Round([double]$parts[1] / 10000.0, 2)
    $small = [math]::Round([double]$parts[2] / 10000.0, 2)
    $mid = [math]::Round([double]$parts[3] / 10000.0, 2)
    $large = [math]::Round([double]$parts[4] / 10000.0, 2)
    $super = [math]::Round([double]$parts[5] / 10000.0, 2)
    $close = $parts[11]
    $pct = $parts[12]

    Write-Host ""
    Write-Host "【交易日期: $date】 收盘价: $close 元 | 涨跌幅: $pct%"
    Write-Host "  主力资金净流入: $main 万元 ($([math]::Round($main/10000.0, 4)) 亿元)"
    Write-Host "  🔴 超大单净流入: $super 万元 ($([math]::Round($super/10000.0, 4)) 亿元)"
    Write-Host "  🟢 大单净流入:   $large 万元 ($([math]::Round($large/10000.0, 4)) 亿元)"
    Write-Host "  中单净流入:     $mid 万元 ($([math]::Round($mid/10000.0, 4)) 亿元)"
    Write-Host "  小单净流入:     $small 万元 ($([math]::Round($small/10000.0, 4)) 亿元)"
}
