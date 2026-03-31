# CP-MES Django

基于 Django 5.0 + PostgreSQL 的生产工单管理系统（MES）。

## 技术栈

- **框架**: Django 5.0 + Django REST Framework
- **数据库**: PostgreSQL 16
- **缓存**: Redis
- **任务队列**: Celery
- **认证**: JWT (djangorestframework-simplejwt)

## 快速开始

### 环境要求

- Python 3.11+
- PostgreSQL 16+
- Redis 7+

### 本地开发

1. **克隆项目**
   ```bash
   cd cp_mes_django
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements/development.txt
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入实际配置
   ```

5. **运行数据库迁移**
   ```bash
   python manage.py migrate
   ```

6. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

7. **运行开发服务器**
   ```bash
   python manage.py runserver
   ```

8. **访问系统**
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Docker 开发

```bash
# 启动开发环境
docker-compose -f docker/docker-compose.dev.yml up -d

# 查看日志
docker-compose -f docker/docker-compose.dev.yml logs -f

# 停止
docker-compose -f docker/docker-compose.dev.yml down
```

### Docker 生产部署

```bash
# 设置环境变量
export DJANGO_SECRET_KEY=your-secret-key
export DB_PASSWORD=your-db-password

# 启动
docker-compose -f docker/docker-compose.yml up -d
```

## 项目结构

```
cp_mes_django/
├── config/                 # 项目配置
│   ├── settings/          # 分环境配置
│   ├── urls.py            # URL 路由
│   └── wsgi.py            # WSGI 入口
├── apps/                   # 应用模块
│   ├── core/              # 核心工具
│   ├── system/            # 系统管理
│   ├── basic_data/        # 基础数据
│   ├── production/        # 生产管理
│   ├── inventory/         # 库存管理
│   ├── report/            # 报表管理
│   └── monitor/           # 系统监控
├── tenants/               # 多租户支持
├── tasks/                 # Celery 任务
├── api/                   # API 版本控制
├── tests/                 # 测试
├── docker/                # Docker 配置
└── requirements/          # 依赖文件
```

## API 文档

启动服务后访问:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## 测试

```bash
# 运行测试
pytest

# 带覆盖率
pytest --cov=apps --cov-report=html
```

## 代码质量

```bash
# 格式化
black apps/ config/ tests/
isort apps/ config/ tests/

# 检查
flake8 apps/ config/ tests/
mypy apps/ config/
```

## 常用命令

```bash
# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 收集静态文件
python manage.py collectstatic

# Django Shell
python manage.py shell

# Celery Worker
celery -A config worker -l info

# Celery Beat
celery -A config beat -l info
```

## 许可证

MIT License
