# 部署指南 - Excel 文件转换系统

## 一、快速开始（本地开发）

### 1. 环境准备
```bash
# 克隆或下载项目
cd excel-converter

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行应用
```bash
python app.py
```

访问：`http://localhost:5000/converter.html`

---

## 二、Linux 服务器部署（推荐方案）

### 1. 系统要求
- Ubuntu 20.04 LTS 或更新版本
- Python 3.8+
- Nginx 1.18+
- 4GB 内存及以上

### 2. 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 和依赖
sudo apt install python3 python3-pip python3-venv -y

# 安装 Nginx
sudo apt install nginx -y

# 安装其他工具
sudo apt install supervisor git -y
```

### 3. 部署应用

```bash
# 创建应用目录
sudo mkdir -p /var/www/excel-converter
cd /var/www/excel-converter

# 下载项目文件（假设使用 git）
sudo git clone <repository-url> .

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建上传目录
mkdir -p uploads
sudo chown www-data:www-data uploads
sudo chmod 755 uploads
```

### 4. 配置 Supervisor

创建文件 `/etc/supervisor/conf.d/excel-converter.conf`：

```ini
[program:excel-converter]
directory=/var/www/excel-converter
command=/var/www/excel-converter/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 --timeout 120 app:app
autostart=true
autorestart=true
user=www-data
environment=PATH="/var/www/excel-converter/venv/bin"
stdout_logfile=/var/log/excel-converter/out.log
stderr_logfile=/var/log/excel-converter/err.log
```

启动 Supervisor：

```bash
# 创建日志目录
sudo mkdir -p /var/log/excel-converter
sudo chown www-data:www-data /var/log/excel-converter

# 重启 Supervisor
sudo systemctl restart supervisor

# 检查状态
sudo supervisorctl status excel-converter
```

### 5. 配置 Nginx

创建文件 `/etc/nginx/sites-available/excel-converter`：

```nginx
upstream flask_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your_domain.com;  # 修改为你的域名

    # 重定向到 HTTPS（可选）
    # return 301 https://$server_name$request_uri;

    client_max_body_size 50M;

    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60;
        proxy_send_timeout 120;
        proxy_read_timeout 120;
    }

    location /uploads {
        alias /var/www/excel-converter/uploads;
        expires 7d;
    }
}
```

启用站点：

```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/excel-converter /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

### 6. 设置 SSL（推荐）

使用 Let's Encrypt：

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your_domain.com

# 自动续期
sudo systemctl enable certbot.timer
```

更新 Nginx 配置为 HTTPS：

```nginx
server {
    listen 443 ssl http2;
    server_name your_domain.com;

    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

    # SSL 配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # ... 其他配置同上
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name your_domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 三、Docker 部署

### 1. 创建 Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用文件
COPY . .

# 创建上传目录
RUN mkdir -p uploads

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
```

### 2. 构建和运行

```bash
# 构建镜像
docker build -t excel-converter:latest .

# 运行容器
docker run -d \
  --name excel-converter \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -e FLASK_ENV=production \
  excel-converter:latest
```

### 3. Docker Compose 配置

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: excel-converter
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - FLASK_ENV=production
    restart: unless-stopped

  nginx:
    image: nginx:latest
    container_name: excel-converter-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./uploads:/var/www/uploads:ro
    depends_on:
      - app
    restart: unless-stopped
```

运行：

```bash
docker-compose up -d
```

---

## 四、安全配置

### 1. 文件安全

```bash
# 限制上传文件大小
# 在 app.py 中已设置 MAX_FILE_SIZE = 10MB

# 设置正确的文件权限
sudo chown www-data:www-data /var/www/excel-converter -R
sudo chmod 755 /var/www/excel-converter
sudo chmod 775 /var/www/excel-converter/uploads
```

### 2. 防火墙规则

```bash
# Ubuntu UFW
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 3. 环境变量配置

创建 `.env` 文件：

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=10485760  # 10MB
```

修改 `app.py` 使用环境变量：

```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 10485760))
```

---

## 五、监控和维护

### 1. 日志管理

```bash
# 查看应用日志
sudo tail -f /var/log/excel-converter/out.log

# 查看错误日志
sudo tail -f /var/log/excel-converter/err.log

# 查看 Nginx 日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. 定期备份

```bash
# 备份上传文件
tar -czf backup_uploads_$(date +%Y%m%d).tar.gz /var/www/excel-converter/uploads/

# 使用 cron 定期备份
# 编辑 crontab
crontab -e

# 添加每日备份任务
0 2 * * * tar -czf /backup/uploads_$(date +\%Y\%m\%d).tar.gz /var/www/excel-converter/uploads/
```

### 3. 健康检查

```bash
# 测试 API 端点
curl http://localhost:5000/health

# 监控磁盘空间
df -h /var/www/excel-converter

# 监控内存使用
free -h
```

---

## 六、故障排查

### 问题 1：502 Bad Gateway

```bash
# 检查 Flask 应用状态
sudo supervisorctl status excel-converter

# 查看错误日志
sudo tail -f /var/log/excel-converter/err.log

# 重启应用
sudo supervisorctl restart excel-converter
```

### 问题 2：文件上传失败

```bash
# 检查权限
ls -la /var/www/excel-converter/uploads/

# 检查磁盘空间
df -h

# 检查最大上传大小配置
# Nginx 和 Flask 都需要配置
```

### 问题 3：转换出错

```bash
# 验证 MANIFEST 文件格式
python test_conversion.py

# 检查 Python 依赖
pip list | grep -E "pandas|openpyxl|Flask"
```

---

## 七、性能优化

### 1. Gunicorn 工作进程优化

```bash
# 计算最佳工作进程数：(2 × CPU 核心数) + 1
# 例如 4 核 CPU：(2 × 4) + 1 = 9

gunicorn -w 9 -b 0.0.0.0:5000 app:app
```

### 2. Nginx 缓存配置

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m;

location / {
    proxy_cache_bypass $http_pragma $http_authorization;
    proxy_pass http://flask_app;
    # ... 其他配置
}
```

### 3. 数据库优化（如果使用）

- 使用连接池
- 添加查询索引
- 定期清理旧文件

---

## 八、更新和维护

### 升级依赖

```bash
# 查看可用更新
pip list --outdated

# 更新所有包
pip install --upgrade -r requirements.txt

# 更新特定包
pip install --upgrade pandas
```

### 更新应用

```bash
# 从 git 拉取最新版本
cd /var/www/excel-converter
sudo git pull origin main

# 安装新的依赖
source venv/bin/activate
pip install -r requirements.txt

# 重启应用
sudo supervisorctl restart excel-converter
```

---

## 联系方式

如有任何部署问题，请联系：

- **公司**：广州翔翔物流有限公司
- **技术支持**：support@xiangxiang-logistics.com
- **紧急联系**：+86-20-XXXX-XXXX

---

最后更新：2025 年 11 月
