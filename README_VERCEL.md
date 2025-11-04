# Excel 文件转换系统 - Vercel 部署版本

**广州翔翔物流有限公司**

## 🚀 快速开始

### 在线访问
https://manifestconversion.vercel.app/

### 本地测试
1. 下载 `index.html` 文件
2. 用浏览器打开即可运行（无需任何服务器）

---

## 📋 功能

- ✅ 拖拽或点击上传 MANIFEST 格式 Excel 文件
- ✅ 自动验证文件格式
- ✅ MANIFEST 到佐川派送模板的数据转换
- ✅ 特殊处理 GOODS 列数据
- ✅ 生成并下载转换后的 Excel 文件
- ✅ 所有处理在浏览器本地完成，数据不上传服务器

---

## 🔧 转换规则详解

### 标准列映射

从 MANIFEST 文件的第 4 行获取映射规则：

| A 文件列 | 说明 | B 文件列 |
|---------|------|---------|
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

### GOODS 列特殊处理（第 I 列）

GOODS 列包含逗号分隔的多个产品信息：

**输入示例**：
```
POLYESTER 100% KNIT ENSEMBLE 1,ELASTANE 1.0% POLYESTER 99.0% WOVEN DRESS 1,ELASTANE 8% VISCOSE 92% KNIT CROP TOP 1,...
```

**处理规则**：
- **Y 列**：第一项的产品名称（去除末尾数字）
  - 结果：`POLYESTER 100% KNIT ENSEMBLE`

- **Z 列**：第一项的末尾数字
  - 结果：`1`

- **AM 列**：从第二项提取产品名+数量，然后追加第三项及后续内容
  - 结果：`WOVEN DRESS 1,ELASTANE 8% VISCOSE 92% KNIT CROP TOP 1,...`

---

## 📁 项目文件

```
project/
├── index.html              # 主应用文件（唯一需要的文件）
├── vercel.json            # Vercel 配置
├── README.md              # 项目说明
└── VERCEL_DEPLOYMENT.md   # 部署指南
```

---

## 🛠️ 技术实现

### 使用的库

- **XLSX.js**（0.18.5）- Excel 文件读写
  - CDN: https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js

### 核心功能

```javascript
// 1. 文件验证
validateManifestFormat(jsonData)
- 检查行数（最少 4 行）
- 检查列数（最少 9 列）
- 验证第 4 行是否有映射标注

// 2. 数据转换
performConversion(jsonData)
- 标准列映射
- GOODS 列特殊处理
- 生成输出数据

// 3. 文件生成
XLSX.utils.aoa_to_sheet()
XLSX.writeFile()
```

---

## ✨ 特色

### 安全性
- 所有数据在浏览器本地处理
- 不涉及任何网络请求
- 用户隐私完全保护

### 易用性
- 直观的拖拽上传界面
- 实时状态反馈
- 友好的错误提示

### 兼容性
- 支持 Chrome、Firefox、Safari、Edge
- 支持 Windows、Mac、Linux
- 支持移动设备（响应式设计）

---

## 🚨 常见问题

**Q: 如何使用？**
A: 
1. 选择或拖拽你的 MANIFEST 格式 Excel 文件
2. 系统自动验证和转换
3. 点击下载按钮获取转换后的文件

**Q: 支持哪些 Excel 格式？**
A: 支持 `.xlsx` 和 `.xls` 格式

**Q: 文件大小有限制吗？**
A: 浏览器可处理的任何大小。理论上支持 100MB+ 的文件

**Q: 我的数据安全吗？**
A: 完全安全。所有处理都在你的浏览器中，数据不会传输到任何服务器

**Q: 离线可以使用吗？**
A: 下载后可以。只需要下载 `index.html` 文件，用浏览器直接打开即可。
   注意：第一次需要在线加载 XLSX 库，之后可以离线使用

**Q: 遇到错误怎么办？**
A: 常见错误及解决方案：
   - "文件行数不足" → 确保是正确的 MANIFEST 格式
   - "列数不足" → 文件可能损坏或格式错误
   - "第 4 行缺少标注" → 检查文件的第 4 行是否有转换规则标注

---

## 📞 支持

- **公司**：广州翔翔物流有限公司
- **邮箱**：support@xiangxiang-logistics.com
- **文档**：查看 VERCEL_DEPLOYMENT.md 获取更多部署信息

---

## 📝 更新历史

### v2.0 (2025-11-04)
- ✅ 改用纯前端架构，支持 Vercel 直接部署
- ✅ 修正 GOODS 列转换规则
- ✅ 集成 XLSX 库进行 Excel 处理
- ✅ 改进 UI/UX 设计

### v1.0 (2025-11-03)
- ✅ Flask 后端 + HTML 前端架构
- ✅ 基础的文件转换功能

---

## ⚖️ 许可证

© 2025 广州翔翔物流有限公司。保留所有权利。

