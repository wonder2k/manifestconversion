# Excel 文件转换系统 - MANIFEST to 佐川模板

## 项目概述

该系统用于将 MANIFEST 格式的 Excel 文件自动转换为佐川派送模板格式。支持在线上传、自动转换和下载功能。

## 主要功能

1. **文件上传**：支持拖拽或点击上传 MANIFEST 格式的 Excel 文件
2. **格式验证**：自动验证上传文件是否符合 MANIFEST 格式
3. **数据转换**：按照预定义的规则将数据转换到佐川模板
4. **特殊处理**：对 GOODS 列进行特殊处理，自动提取产品名称和数量
5. **文件下载**：转换完成后提供 Excel 文件下载

## 技术栈

- **前端**：HTML5 + CSS3 + Vanilla JavaScript
- **后端**：Flask (Python)
- **数据处理**：Pandas + OpenPyXL
- **部署**：Gunicorn + Nginx

## 文件结构

```
.
├── app.py                              # Flask 后端应用
├── converter.html                      # 前端网页
├── MANIFEST-SAMPLE_SHEIN.xlsx         # MANIFEST 格式样本
├── Zuo-Chuan-Pai-Song-Mo-Ban.xlsx     # 佐川模板
├── Zuo-Chuan-Converted-Corrected.xlsx # 转换后的样本
├── requirements.txt                    # Python 依赖
└── README.md                           # 本文件
```

## 本地部署步骤

### 1. 环境要求

- Python 3.8+
- pip 包管理工具
- 现代浏览器

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置文件

确保以下文件在项目根目录：
- `Zuo-Chuan-Pai-Song-Mo-Ban.xlsx` - 佐川模板文件

### 4. 运行应用

**开发环境**：
```bash
python app.py
```

应用将在 `http://localhost:5000` 启动

**生产环境**：
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 5. 访问网页

打开浏览器访问：`http://localhost:5000/converter.html`

## 使用说明

### 步骤 1：上传文件

1. 在左侧框中拖拽 MANIFEST 格式的 Excel 文件，或点击"选择文件"按钮
2. 系统会自动验证文件格式
3. 验证通过后自动开始转换

### 步骤 2：下载文件

1. 转换完成后，右侧框中会出现"下载转换后的文件"按钮
2. 点击按钮下载生成的 Excel 文件

## 转换规则详解

### 标准列映射

根据 MANIFEST 文件第 4 行的标注，将对应列转换到佐川模板：

| MANIFEST 列 | 列名 | 佐川模板列 |
|------------|------|----------|
| 4 | HOUSE AIR WAYBILL NO. | A |
| 6 | WEIGHT | W |
| 9 | IMPORT NAME | AC |
| 11 | TEL NO. | AD |
| 12 | SHIPPER NAME | P |
| 15 | DECLARED VALUE OF CUSTOMS | AB |
| 19 | CONSIGNEE ZIP | AI |
| 37 | SKU | AJ |
| 38 | 商品链接 | AK |
| 39 | HS CODE | AL |

### GOODS 列特殊处理规则（第 I 列）

GOODS 列包含逗号分隔的多个产品信息，按以下规则处理：

**规则说明**：
- 第一项：完整提取（包括材料和产品名称）
  - 提取末尾数字 → 填入 **Z 列**
  - 提取去除末尾数字的部分 → 填入 **Y 列**
- 第二项及后续：
  - 从第二项提取产品名称+数量 → 与后续项拼接填入 **AM 列**

**示例**：

输入（GOODS 列）：
```
POLYESTER 100% KNIT ENSEMBLE 1,ELASTANE 1.0% POLYESTER 99.0% WOVEN DRESS 1,ELASTANE 8% VISCOSE 92% KNIT CROP TOP 1,...
```

转换结果：
- **Y 列**：`POLYESTER 100% KNIT ENSEMBLE`
- **Z 列**：`1`
- **AM 列**：`WOVEN DRESS 1,ELASTANE 8% VISCOSE 92% KNIT CROP TOP 1,...`

## API 文档

### POST /api/convert

上传并转换 Excel 文件

**请求**：
- 方法：POST
- Content-Type：multipart/form-data
- 参数：`file` (Excel 文件)

**响应**（成功）：
- 状态码：200
- Body：转换后的 Excel 文件（二进制）

**响应**（失败）：
```json
{
  "success": false,
  "message": "错误信息"
}
```

### POST /api/validate

仅验证文件格式（不进行转换）

**请求**：
- 方法：POST
- Content-Type：multipart/form-data
- 参数：`file` (Excel 文件)

**响应**：
```json
{
  "success": true/false,
  "message": "验证结果信息"
}
```

### GET /health

健康检查

**响应**：
```json
{
  "status": "ok",
  "message": "Server is running"
}
```

## 错误处理

系统会捕获并反馈以下常见错误：

1. **文件格式错误**：上传的不是 Excel 文件
2. **MANIFEST 格式不符**：缺少必要的行或列
3. **读取错误**：Excel 文件损坏或无法读取
4. **转换错误**：数据处理过程中的异常

## 部署到生产环境

### 使用 Nginx + Gunicorn

**1. 配置 Gunicorn**：
```bash
gunicorn -w 4 -b 127.0.0.1:5000 --timeout 120 app:app
```

**2. Nginx 配置**（示例）：
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads {
        alias /path/to/app/uploads;
    }
}
```

### 使用 Docker

创建 `Dockerfile`：
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

构建和运行：
```bash
docker build -t excel-converter .
docker run -p 5000:5000 excel-converter
```

## 常见问题

**Q：上传文件时显示"文件格式错误"**
A：请确保上传的是 MANIFEST 格式的 Excel 文件，且包含至少 4 行和 9 列数据。

**Q：转换后的文件为空**
A：可能是源文件没有数据行。请检查 MANIFEST 文件是否有从第 2 行开始的数据。

**Q：如何确认 MANIFEST 格式是否正确？**
A：检查以下要点：
- 第 1 行：列标题
- 第 2 行：示例数据
- 第 3 行：通常为空
- 第 4 行：标注转换规则（显示对应的佐川模板列号）

## 联系方式

如有问题或建议，请联系：
- 公司：广州吉成物流有限公司
- 邮箱：support@JC-logistics.com
- 电话：+86-20-XXXX-XXXX

## 许可证

© 2025 广州吉成物流有限公司。保留所有权利。
