# cp-mes-ruoyi

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-2.7.9-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Vue](https://img.shields.io/badge/Vue-2.6.12-brightgreen.svg)](https://vuejs.org/)

> 基于RuoYi开发的生产工单管理系统（MES），适用于中小型生产企业的生产过程管理。

---

## 目录

- [项目介绍](#项目介绍)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [部署指南](#部署指南)
- [在线体验](#在线体验)
- [界面展示](#界面展示)
- [技术交流](#技术交流)
- [许可证](#许可证)

---

## 项目介绍

本项目是基于RuoYi框架开发的生产工单管理系统（MES），权限部分沿用了框架自带的体系，其余功能为定制开发，UI样式做了全面改造。

系统提供了一系列生产管理的功能，适用于中小型生产型企业，满足用户对生产过程的管理需求。

**个人和企业均可免费自用，但禁止售卖代码获利。**

---

## 技术栈

### 后端技术

| 技术 | 版本 | 说明 |
| --- | --- | --- |
| Spring Boot | 2.7.9 | 应用框架 |
| Sa-Token | 1.34.0 | 权限认证（JWT模式） |
| MyBatis-Plus | 3.5.3.1 | ORM框架 |
| Redisson | 3.20.0 | Redis客户端 |
| Hutool | 5.8.15 | Java工具库 |
| EasyExcel | 3.2.1 | Excel处理 |
| XXL-Job | 2.3.1 | 分布式任务调度 |
| Swagger | 3.0.0 | API文档 |

### 前端技术

| 技术 | 版本 | 说明 |
| --- | --- | --- |
| Vue | 2.6.12 | 前端框架 |
| Element-UI | 2.15.12 | UI组件库 |
| Vuex | 3.6.0 | 状态管理 |
| Vue Router | 3.4.9 | 路由管理 |
| Axios | 0.24.0 | HTTP请求 |
| ECharts | 5.4.0 | 图表库 |

### 数据库支持

- MySQL（默认）
- Oracle
- PostgreSQL
- SQL Server
- TDengine

---

## 项目结构

```
cp-mes-ruoyi
├── cp-mes-admin         # 主应用入口（Web服务）
├── cp-mes-common        # 公共模块（工具类、注解、常量、异常）
├── cp-mes-framework     # 核心框架配置（Redis、MyBatis、安全等）
├── cp-mes-system        # 系统模块（实体、Mapper、Service）
├── cp-mes-generator     # 代码生成器模块
├── cp-mes-job           # 定时任务模块
├── cp-mes-oss           # 对象存储服务模块
├── cp-mes-sms           # 短信服务模块
├── cp-mes-demo          # 示例模块
├── cp-mes-extend        # 扩展模块（监控、XXL-Job管理）
├── cp-mes-ui            # 前端Vue应用
├── script               # 脚本文件
│   └── sql              # 数据库初始化脚本
└── doc                  # 文档和截图
```

---

## 功能特性

### 核心业务功能

| 模块 | 功能说明 |
| --- | --- |
| **基础数据** | 客户管理、不良项管理、生产工序、工艺路线、产品信息 |
| **生产管理** | 生产工单管理、任务分配、报工操作、生产进度跟踪 |
| **库存管理** | 物料管理、供应商管理、出入库操作、库存盘点 |
| **报表管理** | 产量统计、不良项分析、生产报表、数据导出 |
| **数据看板** | 大屏展示、数据概览、实时监控 |

### 系统管理功能

| 功能 | 说明 |
| --- | --- |
| 用户管理 | 用户增删改查、分配角色、重置密码 |
| 角色管理 | 角色权限配置、数据权限 |
| 部门管理 | 组织架构管理 |
| 菜单管理 | 菜单配置、按钮权限 |
| 字典管理 | 系统字典数据维护 |
| 参数设置 | 系统参数配置 |
| 日志管理 | 登录日志、操作日志 |
| 在线用户 | 在线用户监控、强制下线 |
| 代码生成 | 在线生成业务代码 |

### 进阶功能

- **自定义字段**：动态扩展业务实体字段
- **自定义报表**：灵活配置统计报表
- **多数据源**：支持多数据库切换
- **多租户**：支持多租户数据隔离

### 其他功能

- 个人信息管理
- 深浅主题切换
- 平台工单反馈
- 消息通知

---

## 快速开始

### 环境要求

- JDK 1.8+
- Maven 3.6+
- MySQL 5.7+
- Redis 3.0+
- Node.js 14+

### 后端启动

1. **克隆项目**
   ```bash
   git clone https://github.com/xxx/cp-mes-ruoyi.git
   cd cp-mes-ruoyi
   ```

2. **导入数据库**
   ```bash
   mysql -u root -p < script/sql/cp_mes.sql
   ```

3. **修改配置**
   
   编辑 `cp-mes-admin/src/main/resources/application-dev.yml`：
   ```yaml
   # 数据库配置
   spring:
     datasource:
       url: jdbc:mysql://localhost:3306/cp_mes?useUnicode=true&characterEncoding=utf8
       username: root
       password: your_password
   
   # Redis配置
   redis:
     host: localhost
     port: 6379
     password: your_redis_password
   ```

4. **启动后端**
   ```bash
   # 方式一：Maven启动
   mvn clean install
   cd cp-mes-admin
   mvn spring-boot:run
   
   # 方式二：IDE启动
   运行 CpMesApplication.java 主类
   ```

### 前端启动

1. **安装依赖**
   ```bash
   cd cp-mes-ui
   npm install
   ```

2. **启动开发服务器**
   ```bash
   npm run dev
   ```

3. **访问系统**
   
   浏览器访问：http://localhost:80

### 默认账号

| 账号 | 密码 | 角色 |
| --- | --- | --- |
| admin | admin123 | 超级管理员 |

---

## 配置说明

### 后端配置文件

| 文件 | 说明 |
| --- | --- |
| `application.yml` | 主配置文件 |
| `application-dev.yml` | 开发环境配置 |
| `application-prod.yml` | 生产环境配置 |

### 主要配置项

```yaml
# 服务端口
server:
  port: 8090

# 数据库（支持MySQL、Oracle、PostgreSQL等）
spring:
  datasource:
    dynamic:
      datasource:
        master:
          url: jdbc:mysql://localhost:3306/cp_mes
          username: root
          password: password

# Redis配置
redis:
  host: localhost
  port: 6379

# Sa-Token配置
sa-token:
  token-name: Authorization
  timeout: 2592000
```

### 前端配置

编辑 `cp-mes-ui/vue.config.js` 配置后端代理：

```javascript
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8090',
        changeOrigin: true
      }
    }
  }
}
```

---

## 部署指南

### Docker部署

```bash
# 构建镜像
docker build -t cp-mes:latest .

# 运行容器
docker run -d \
  --name cp-mes \
  -p 8090:8090 \
  -e MYSQL_HOST=localhost \
  -e MYSQL_PORT=3306 \
  -e REDIS_HOST=localhost \
  cp-mes:latest
```

### JAR包部署

```bash
# 打包
mvn clean package -Dmaven.test.skip=true

# 运行
java -jar cp-mes-admin/target/cp-mes-admin.jar --spring.profiles.active=prod
```

### Nginx配置

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/cp-mes-ui/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:8090/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 在线体验

- **演示地址**：http://cp-mes.cn
- **体验账号**：18000000000 / abc123456
- 如需单独账号体验，请添加底部微信联系

---

## 界面展示

### 浅色主题

<img src='doc/pics/界面截图一.png' width='600'>
<img src='doc/pics/界面截图二.png' width='600'>
<img src='doc/pics/界面截图三.png' width='600'>
<img src='doc/pics/界面截图四.png' width='600'>
<img src='doc/pics/界面截图五.png' width='600'>

### 深色主题

<img src='doc/pics/界面截图六.png' width='600'>

---

## 技术交流

### 运行文档

详细运行文档请查看：[飞书文档](https://to6tvs3h8n.feishu.cn/wiki/GhQ7wDMoOiTS6tk6O5scnwAonVd?from=from_copylink)

### 公众号

关注"云脉软件"公众号，获取更多案例和教程：

<img src='doc/pics/公众号二维码.jpg' width='200'>

### 微信交流

咨询交流请加微信：

<img src='doc/pics/联系人二维码.jpg' width='200'>

---

## 关于我们

**苏州云脉软件技术有限公司**

官网：[www.szcloudpulse.com](https://www.szcloudpulse.com)

---

## 许可证

本项目采用 MIT 许可证，个人和企业均可免费自用，但**禁止售卖代码获利**。

---

## Star History

如果这个项目对您有帮助，请点个 Star 支持一下！

持续开发中，欢迎关注项目动态。
