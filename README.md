# china-holiday

中国法定节假日数据，自动抓取国务院公告。

## 功能

- 提供 JSON 格式节假日数据（2016年至今）
- 提供 ICalendar 格式节假日数据（2016年至今）
- GitHub Actions 自动更新
- 数据变化时自动发布新版本
- 提供 all.json 和 all.ics 整合文件

## 数据格式

单年数据格式：

```json
{
  "year": 2025,
  "papers": ["https://www.gov.cn/zhengce/zhengceku/202411/content_6986383.htm"],
  "days": [
    {
      "name": "元旦",
      "date": "2025-01-01",
      "isOffDay": true
    }
  ]
}
```

所有年份整合数据格式：

```json
{
  "years": {
    "start": 2016,
    "end": 2027
  },
  "papers": ["https://www.gov.cn/zhengce/zhengceku/202411/content_6986383.htm"],
  "days": [
    {
      "name": "元旦",
      "date": "2025-01-01",
      "isOffDay": true
    }
  ]
}
```

## 通过互联网使用

### GitHub Raw（推荐使用 CDN）

单年 JSON 数据地址：
```
https://raw.githubusercontent.com/lwx-cloud/china-holiday/main/{年份}.json
```

单年 ICalendar 订阅地址：
```
https://raw.githubusercontent.com/lwx-cloud/china-holiday/main/{年份}.ics
```

所有年份整合 JSON 数据地址：
```
https://raw.githubusercontent.com/lwx-cloud/china-holiday/main/all.json
```

所有年份整合 ICalendar 订阅地址：
```
https://raw.githubusercontent.com/lwx-cloud/china-holiday/main/all.ics
```

### jsDelivr CDN（高速访问）

单年 JSON 数据地址：
```
https://cdn.jsdelivr.net/gh/lwx-cloud/china-holiday@main/{年份}.json
```

单年 ICalendar 订阅地址：
```
https://cdn.jsdelivr.net/gh/lwx-cloud/china-holiday@main/{年份}.ics
```

所有年份整合 JSON 数据地址：
```
https://cdn.jsdelivr.net/gh/lwx-cloud/china-holiday@main/all.json
```

所有年份整合 ICalendar 订阅地址：
```
https://cdn.jsdelivr.net/gh/lwx-cloud/china-holiday@main/all.ics
```

### 使用特定版本

使用 release 版本（需先在 GitHub 创建 release）：
```
https://cdn.jsdelivr.net/gh/lwx-cloud/china-holiday@{版本号}/{年份}.json
```

## 本地运行

```bash
pip install -r requirements.txt
python scripts/fetch.py 2025
```

## 开发

```bash
pip install -r dev-requirements.txt
make format
make lint
make test
```
