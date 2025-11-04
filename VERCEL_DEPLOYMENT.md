# Vercel 快速部署指南

## 问题原因

原始 Flask 后端应用无法直接在 Vercel 上部署，因为：
1. Vercel 免费版主要针对静态网站和 Node.js 应用
2. Python Flask 在 Vercel 上的支持有限且需要特殊配置
3. 出现 404 错误是因为无法正确处理 Flask 路由

## 解决方案

已为你创建了**完全前端版本**，所有转换逻辑都在浏览器中运行：

- ✓ 无需后端服务器
- ✓ 支持直接在 Vercel 静态部署
- ✓ 所有数据在浏览器本地处理，不上传服务器
- ✓ 更快的性能和更低的成本

## 部署步骤

### 1. 更新 GitHub 仓库

```bash
# 使用新的 index.html 替换原有的 converter.html
# 删除 app.py（不再需要）
# 保留 vercel.json 配置文件
```

### 2. 仓库文件结构

```
your-repo/
├── index.html              # 新的前端应用（重要！）
├── vercel.json            # Vercel 配置
└── README.md              # 项目说明（可选）
```

### 3. Vercel 部署步骤

**方法 A：通过 Vercel Dashboard（推荐）**

1. 访问 https://vercel.com/dashboard
2. 点击 "New Project"
3. 选择你的 GitHub 仓库
4. 框架选择：`Other`（因为这是纯前端 HTML）
5. 设置不做任何改变，直接点击 "Deploy"

**方法 B：命令行部署**

```bash
npm install -g vercel
vercel
```

### 4. 验证部署

- 访问 https://manifestconversion.vercel.app/
- 应该能看到 Excel 转换网页
- 测试上传和转换功能

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 主应用文件，包含所有 HTML、CSS 和 JavaScript |
| `vercel.json` | Vercel 配置文件 |

## 功能特点

✓ 完全在浏览器中运行转换
✓ 支持 Excel 文件读写（使用 XLSX.js）
✓ MANIFEST 格式验证
✓ GOODS 列特殊处理
✓ 实时进度显示
✓ 错误提示和状态显示

## 常见问题

**Q: 为什么没有后端服务器？**
A: 所有转换逻辑已整合到前端，用户上传的文件在浏览器中处理，不需要服务器。

**Q: 数据安全吗？**
A: 是的。所有数据都在用户的浏览器中处理，不会上传到任何服务器。

**Q: 如果我想要后端版本怎么办？**
A: 可以使用 Heroku、Railway 或其他支持 Python 的平台部署 Flask 应用。

## 下一步

如果部署后出现任何问题：

1. 检查 Vercel Dashboard 中的部署日志
2. 在浏览器控制台查看 JavaScript 错误
3. 验证 index.html 文件是否正确上传

---

支持联系：support@xiangxiang-logistics.com
