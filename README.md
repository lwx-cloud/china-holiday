# china-holiday

中国法定节假日数据，自动抓取国务院公告。

## 功能

- 提供 JSON 格式节假日数据
- 提供 ICalendar 格式节假日数据
- GitHub Actions 自动更新
- 数据变化时自动发布新版本

## 数据格式

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

## 通过互联网使用

JSON 数据地址：
```
https://raw.githubusercontent.com/lwx-cloud/china-holiday/main/{年份}.json
```

ICalendar 订阅地址：
```
https://raw.githubusercontent.com/lwx-cloud/china-holiday/main/{年份}.ics
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
