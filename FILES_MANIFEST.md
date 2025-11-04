# 项目文件清单

## 核心应用文件

### 1. app.py
**功能**：Flask 后端应用主程序
**功能点**：
- 实现 `/api/convert` 接口，处理文件上传和转换
- 实现 `/api/validate` 接口，验证 MANIFEST 格式
- 实现 `/health` 接口，健康检查
- 包含完整的文件验证和错误处理逻辑
- 支持 CORS 跨域请求

**核心函数**：
- `validate_manifest_format(df)` - 验证 MANIFEST 格式
- `convert_file_a_to_b(input_df, template_file_path)` - 执行文件转换

---

### 2. converter.html
**功能**：前端网页界面
**功能点**：
- 左侧区域：拖拽或点击上传 MANIFEST 文件
- 右侧区域：显示下载按钮
- 实时显示处理状态和错误提示
- 响应式设计，支持移动设备

**前端特性**：
- 拖拽上传
- 文件信息显示
- 加载动画
- 状态提示（成功/错误/信息）
- 现代化 UI 设计

---

### 3. converter.html (备选方案)
配合 `app.py` 的后端 API 端点工作

---

## 配置和依赖文件

### 4. requirements.txt
**功能**：Python 依赖声明
**包含**：
- Flask 2.3.3 - Web 框架
- Flask-CORS 4.0.0 - 跨域支持
- Pandas 2.0.3 - Excel 数据处理
- OpenPyXL 3.1.2 - Excel 文件操作
- Werkzeug 2.3.7 - WSGI 工具
- python-dotenv 1.0.0 - 环境变量管理
- Gunicorn 21.2.0 - 生产服务器

**安装方式**：
```bash
pip install -r requirements.txt
```

---

## 测试和验证文件

### 5. test_conversion.py
**功能**：自动化测试脚本
**测试项**：
- GOODS 列转换逻辑验证
  - Y 列提取（去除数字的产品名称）
  - Z 列提取（末尾数字）
  - AM 列提取（后续产品信息）
- 文件存在性检查
- MANIFEST 格式验证
- 文件列数和行数检查

**运行方式**：
```bash
python test_conversion.py
```

**预期输出**：
- 所有 GOODS 列转换测试通过 ✓
- 所有文件转换测试通过 ✓

---

## 文档文件

### 6. README.md
**功能**：项目总体说明文档
**包含内容**：
- 项目概述
- 功能介绍
- 技术栈说明
- 本地部署步骤
- 使用说明
- 转换规则详解
- API 文档
- 错误处理说明
- 部署到生产环境的初步指引

---

### 7. DEPLOYMENT.md
**功能**：详细的部署和运维指南
**包含内容**：
- 快速开始（本地开发）
- Linux 服务器部署（完整步骤）
  - 系统要求
  - 安装依赖
  - Supervisor 配置
  - Nginx 配置
  - SSL 设置
- Docker 部署
  - Dockerfile 编写
  - Docker Compose 配置
- 安全配置
  - 文件安全
  - 防火墙规则
  - 环境变量管理
- 监控和维护
  - 日志管理
  - 备份策略
  - 健康检查
- 故障排查
  - 常见问题及解决方案
- 性能优化
  - Gunicorn 优化
  - Nginx 缓存
- 更新和维护

---

## 示例数据文件

### 8. MANIFEST-SAMPLE_SHEIN.xlsx
**功能**：MANIFEST 格式样本文件
**内容**：
- 第 1 行：列标题
- 第 2 行：实际数据示例（来自 SHEIN）
- 第 3 行：空行
- 第 4 行：转换规则标注
- 包含 40 列数据

**使用场景**：
- 用于理解 MANIFEST 格式
- 用于测试和验证转换逻辑

---

### 9. Zuo-Chuan-Pai-Song-Mo-Ban.xlsx
**功能**：佐川派送模板（目标格式）
**内容**：
- 第 1 行：列标题
- 第 2 行：示例数据
- 包含 35 列数据（A 到 AI）

**使用场景**：
- 作为转换的目标模板
- 定义输出文件的结构

---

### 10. Zuo-Chuan-Converted-Corrected.xlsx
**功能**：转换完成后的输出示例
**内容**：
- 转换后的数据示例
- 展示正确的转换结果

**用途**：
- 参考转换结果
- 验证转换逻辑是否正确

---

## 快速开始

### 本地开发

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行测试
python test_conversion.py

# 3. 启动应用
python app.py

# 4. 访问网页
# 浏览器打开：http://localhost:5000/converter.html
```

### Linux 服务器部署

参考 `DEPLOYMENT.md` 的"二、Linux 服务器部署"部分

### Docker 部署

参考 `DEPLOYMENT.md` 的"三、Docker 部署"部分

---

## 文件关系图

```
┌─────────────────────────────────────────────────┐
│  用户访问 converter.html (前端网页)               │
└────────────────┬────────────────────────────────┘
                 │ 上传文件
                 ▼
┌─────────────────────────────────────────────────┐
│  Flask app.py (后端应用)                        │
│  ├─ POST /api/convert 处理转换                  │
│  └─ validate_manifest_format 验证格式          │
└────────────────┬────────────────────────────────┘
                 │ 读取模板
                 ▼
         ┌───────────────────┐
         │ MANIFEST 输入文件  │
         │ (MANIFEST-SAMPLE) │
         └───────────────────┘
                 │
                 │ 转换逻辑
                 │ ├─ 标准列映射
                 │ └─ GOODS 特殊处理
                 │    ├─ Y 列提取
                 │    ├─ Z 列提取
                 │    └─ AM 列提取
                 ▼
         ┌───────────────────┐
         │ 佐川模板 (输出)     │
         │ (Zuo-Chuan-...)   │
         └───────────────────┘
                 │
                 └─▶ 返回给用户下载
```

---

## 维护说明

### 定期任务

1. **日志检查**（每周）
   ```bash
   tail -f /var/log/excel-converter/err.log
   ```

2. **磁盘空间检查**（每周）
   ```bash
   df -h /var/www/excel-converter
   ```

3. **依赖更新**（每月）
   ```bash
   pip list --outdated
   ```

4. **备份**（每日自动）
   - 上传文件定期清理
   - 数据库备份（如适用）

### 版本更新

- 更新依赖时运行 `python test_conversion.py` 验证
- 修改转换逻辑后必须更新 GOODS 列处理部分
- 部署前在测试环境验证

---

## 故障恢复

### 快速重启

```bash
# 方法 1：使用 Supervisor
sudo supervisorctl restart excel-converter

# 方法 2：使用 Systemd
sudo systemctl restart excel-converter

# 方法 3：Docker
docker restart excel-converter
```

### 重置应用

```bash
# 清空上传文件
sudo rm -rf /var/www/excel-converter/uploads/*

# 重启应用
sudo supervisorctl restart excel-converter
```

---

最后更新：2025 年 11 月 3 日
转换逻辑版本：2.0（已修正 GOODS 列处理）
