# Database Migration Mapping

## 1. Overview

This document maps all MySQL tables to PostgreSQL/Django ORM models.

### Source Database
- **Type:** MySQL 5.7
- **Schema:** cp_mes
- **Charset:** utf8mb4

### Target Database
- **Type:** PostgreSQL 16
- **Schema:** public (with tenant schemas)
- **Encoding:** UTF8

---

## 2. Table Mapping Summary

| # | MySQL Table | Django Model | App | Description |
|---|-------------|--------------|-----|-------------|
| 1 | `attachment_info` | AttachmentInfo | inventory | 附件信息 |
| 2 | `client` | Client | basic_data | 客户信息 |
| 3 | `custom_info` | CustomInfo | system | 自定义字段 |
| 4 | `custom_report` | CustomReport | report | 自定义报表 |
| 5 | `defect` | Defect | basic_data | 不良项 |
| 6 | `example_report` | ExampleReport | report | 例报管理 |
| 7 | `field` | Field | report | 自定义报表字段 |
| 8 | `gen_table` | GenTable | system | 代码生成表 |
| 9 | `gen_table_column` | GenTableColumn | system | 代码生成字段 |
| 10 | `job_booking` | JobBooking | production | 报工记录 |
| 11 | `logo_info` | LogoInfo | system | Logo信息 |
| 12 | `material` | Material | inventory | 物料 |
| 13 | `platform_order` | PlatformOrder | system | 平台工单 |
| 14 | `procedure_info` | Procedure | basic_data | 工序 |
| 15 | `process_route` | ProcessRoute | basic_data | 工艺路线 |
| 16 | `product` | Product | basic_data | 产品 |
| 17 | `purveyor_info` | Supplier | inventory | 供应商 |
| 18 | `sheet` | Sheet | production | 生产工单 |
| 19 | `sheet_material` | SheetMaterial | inventory | 工单物料 |
| 20 | `sys_config` | Config | system | 系统配置 |
| 21 | `sys_dept` | Dept | system | 部门 |
| 22 | `sys_dict_data` | DictData | system | 字典数据 |
| 23 | `sys_dict_type` | DictType | system | 字典类型 |
| 24 | `sys_logininfor` | LoginLog | system | 登录日志 |
| 25 | `sys_menu` | Menu | system | 菜单 |
| 26 | `sys_notice` | Notice | system | 通知公告 |
| 27 | `sys_oper_log` | OperLog | system | 操作日志 |
| 28 | `sys_oss` | Oss | system | 对象存储 |
| 29 | `sys_oss_config` | OssConfig | system | OSS配置 |
| 30 | `sys_post` | Post | system | 岗位 |
| 31 | `sys_role` | Role | system | 角色 |
| 32 | `sys_role_dept` | RoleDept | system | 角色部门关联 |
| 33 | `sys_role_menu` | RoleMenu | system | 角色菜单关联 |
| 34 | `sys_tenant` | Tenant | tenants | 租户 |
| 35 | `sys_tenant_package` | TenantPackage | tenants | 租户套餐 |
| 36 | `sys_user` | User | system | 用户 |
| 37 | `sys_user_post` | UserPost | system | 用户岗位关联 |
| 38 | `sys_user_role` | UserRole | system | 用户角色关联 |
| 39 | `task` | Task | production | 任务 |

---

## 3. Data Type Mapping

### MySQL to PostgreSQL Type Conversion

| MySQL Type | PostgreSQL Type | Django Field |
|------------|-----------------|--------------|
| `bigint(20)` | `BIGINT` | `BigIntegerField` |
| `int(11)` | `INTEGER` | `IntegerField` |
| `smallint(6)` | `SMALLINT` | `SmallIntegerField` |
| `tinyint(4)` | `SMALLINT` | `SmallIntegerField` |
| `varchar(n)` | `VARCHAR(n)` | `CharField(max_length=n)` |
| `char(n)` | `CHAR(n)` | `CharField(max_length=n)` |
| `text` | `TEXT` | `TextField()` |
| `longtext` | `TEXT` | `TextField()` |
| `datetime` | `TIMESTAMP WITH TIME ZONE` | `DateTimeField()` |
| `date` | `DATE` | `DateField()` |
| `time` | `TIME` | `TimeField()` |
| `decimal(m,n)` | `NUMERIC(m,n)` | `DecimalField(max_digits=m, decimal_places=n)` |
| `double` | `DOUBLE PRECISION` | `FloatField()` |
| `float` | `REAL` | `FloatField()` |

---

## 4. Detailed Model Definitions

### 4.1 System Module

#### User (sys_user)

```python
# apps/system/models/user.py

class User(AbstractBaseUser):
    """用户表"""
    id = models.BigAutoField(primary_key=True)
    dept_id = models.BigIntegerField(null=True, blank=True)
    user_name = models.CharField(max_length=30, unique=True, db_column='user_name')
    nick_name = models.CharField(max_length=30)
    user_type = models.CharField(max_length=10, default='sys_user')
    email = models.CharField(max_length=50, null=True, blank=True)
    phonenumber = models.CharField(max_length=11, null=True, blank=True)
    sex = models.CharField(max_length=1, default='0')  # 0=男, 1=女, 2=未知
    avatar = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100)
    status = models.CharField(max_length=1, default='0')  # 0=正常, 1=停用
    del_flag = models.CharField(max_length=1, default='0')  # 0=存在, 2=删除
    login_ip = models.CharField(max_length=128, null=True, blank=True)
    login_date = models.DateTimeField(null=True, blank=True)
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    # Relationships
    dept = models.ForeignKey('Dept', on_delete=models.SET_NULL, null=True, blank=True)
    roles = models.ManyToManyField('Role', through='UserRole')
    posts = models.ManyToManyField('Post', through='UserPost')
    
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['nick_name']
    
    class Meta:
        db_table = 'sys_user'
```

#### Role (sys_role)

```python
# apps/system/models/role.py

class Role(models.Model):
    """角色表"""
    id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=30)
    role_key = models.CharField(max_length=100)
    role_sort = models.IntegerField(default=0)
    data_scope = models.CharField(max_length=1, default='1')
    menu_check_strictly = models.BooleanField(default=True)
    dept_check_strictly = models.BooleanField(default=True)
    status = models.CharField(max_length=1, default='0')
    del_flag = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    # Relationships
    menus = models.ManyToManyField('Menu', through='RoleMenu')
    depts = models.ManyToManyField('Dept', through='RoleDept')
    
    class Meta:
        db_table = 'sys_role'
```

#### Menu (sys_menu)

```python
# apps/system/models/menu.py

class Menu(models.Model):
    """菜单表"""
    id = models.BigAutoField(primary_key=True)
    menu_name = models.CharField(max_length=50)
    parent_id = models.BigIntegerField(default=0)
    order_num = models.IntegerField(default=0)
    path = models.CharField(max_length=200, null=True, blank=True)
    component = models.CharField(max_length=255, null=True, blank=True)
    query = models.CharField(max_length=255, null=True, blank=True)
    route_name = models.CharField(max_length=50, null=True, blank=True)
    is_frame = models.CharField(max_length=1, default='1')
    is_cache = models.CharField(max_length=1, default='0')
    menu_type = models.CharField(max_length=1, default='M')  # M=目录, C=菜单, F=按钮
    visible = models.CharField(max_length=1, default='0')
    status = models.CharField(max_length=1, default='0')
    perms = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=100, default='#')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = 'sys_menu'
```

#### Dept (sys_dept)

```python
# apps/system/models/dept.py

class Dept(models.Model):
    """部门表"""
    id = models.BigAutoField(primary_key=True)
    parent_id = models.BigIntegerField(default=0)
    ancestors = models.CharField(max_length=50, default='')
    dept_name = models.CharField(max_length=30)
    order_num = models.IntegerField(default=0)
    leader = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=1, default='0')
    del_flag = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'sys_dept'
```

#### Post (sys_post)

```python
# apps/system/models/post.py

class Post(models.Model):
    """岗位表"""
    id = models.BigAutoField(primary_key=True)
    post_code = models.CharField(max_length=64)
    post_name = models.CharField(max_length=50)
    post_sort = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'sys_post'
```

#### Config (sys_config)

```python
# apps/system/models/config.py

class Config(models.Model):
    """系统配置表"""
    id = models.BigAutoField(primary_key=True)
    config_name = models.CharField(max_length=100)
    config_key = models.CharField(max_length=100, unique=True)
    config_value = models.CharField(max_length=500)
    config_type = models.CharField(max_length=1, default='N')  # Y=系统内置, N=非内置
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'sys_config'
```

#### DictType (sys_dict_type)

```python
# apps/system/models/dict.py

class DictType(models.Model):
    """字典类型表"""
    id = models.BigAutoField(primary_key=True)
    dict_name = models.CharField(max_length=100)
    dict_type = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'sys_dict_type'


class DictData(models.Model):
    """字典数据表"""
    id = models.BigAutoField(primary_key=True)
    dict_sort = models.IntegerField(default=0)
    dict_label = models.CharField(max_length=100)
    dict_value = models.CharField(max_length=100)
    dict_type = models.CharField(max_length=100)
    css_class = models.CharField(max_length=100, null=True, blank=True)
    list_class = models.CharField(max_length=100, null=True, blank=True)
    is_default = models.CharField(max_length=1, default='N')
    status = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = 'sys_dict_data'
```

#### OperLog (sys_oper_log)

```python
# apps/system/models/oper_log.py

class OperLog(models.Model):
    """操作日志表"""
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    business_type = models.IntegerField(default=0)
    method = models.CharField(max_length=200)
    request_method = models.CharField(max_length=10, null=True, blank=True)
    operator_type = models.IntegerField(default=0)
    oper_name = models.CharField(max_length=50, null=True, blank=True)
    dept_name = models.CharField(max_length=50, null=True, blank=True)
    oper_url = models.CharField(max_length=255, null=True, blank=True)
    oper_ip = models.CharField(max_length=128, null=True, blank=True)
    oper_location = models.CharField(max_length=255, null=True, blank=True)
    oper_param = models.TextField(null=True, blank=True)
    json_result = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=0)
    error_msg = models.TextField(null=True, blank=True)
    oper_time = models.DateTimeField(auto_now_add=True)
    cost_time = models.BigIntegerField(default=0)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'sys_oper_log'
```

#### LoginLog (sys_logininfor)

```python
# apps/system/models/login_log.py

class LoginLog(models.Model):
    """登录日志表"""
    id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=50, null=True, blank=True)
    ipaddr = models.CharField(max_length=128, null=True, blank=True)
    login_location = models.CharField(max_length=255, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
    os = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=1, default='0')
    msg = models.CharField(max_length=255, null=True, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'sys_logininfor'
```

### 4.2 Basic Data Module

#### Client (client)

```python
# apps/basic_data/models/client.py

class Client(models.Model):
    """客户表"""
    id = models.BigAutoField(primary_key=True)
    client_code = models.CharField(max_length=50, unique=True)
    client_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'client'
```

#### Product (product)

```python
# apps/basic_data/models/product.py

class Product(models.Model):
    """产品表"""
    id = models.BigAutoField(primary_key=True)
    product_code = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=50, null=True, blank=True)
    specification = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'product'
```

#### Procedure (procedure_info)

```python
# apps/basic_data/models/procedure.py

class Procedure(models.Model):
    """工序表"""
    id = models.BigAutoField(primary_key=True)
    procedure_code = models.CharField(max_length=50, unique=True)
    procedure_name = models.CharField(max_length=100)
    procedure_type = models.CharField(max_length=50, null=True, blank=True)
    standard_time = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'procedure_info'
```

#### ProcessRoute (process_route)

```python
# apps/basic_data/models/process_route.py

class ProcessRoute(models.Model):
    """工艺路线表"""
    id = models.BigAutoField(primary_key=True)
    route_code = models.CharField(max_length=50, unique=True)
    route_name = models.CharField(max_length=100)
    product_id = models.BigIntegerField(null=True, blank=True)
    procedures = models.JSONField(default=list)  # 工序列表
    status = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'process_route'
```

#### Defect (defect)

```python
# apps/basic_data/models/defect.py

class Defect(models.Model):
    """不良项表"""
    id = models.BigAutoField(primary_key=True)
    defect_code = models.CharField(max_length=50, unique=True)
    defect_name = models.CharField(max_length=100)
    defect_type = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'defect'
```

### 4.3 Production Module

#### Sheet (sheet)

```python
# apps/production/models/sheet.py

class Sheet(models.Model):
    """生产工单表"""
    id = models.BigAutoField(primary_key=True)
    sheet_code = models.CharField(max_length=50, unique=True)
    sheet_name = models.CharField(max_length=200)
    product_id = models.BigIntegerField()
    product_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    completed_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    defect_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, default='0')  # 0=待生产, 1=生产中, 2=已完成, 3=已取消
    priority = models.IntegerField(default=0)
    process_route_id = models.BigIntegerField(null=True, blank=True)
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'sheet'
```

#### Task (task)

```python
# apps/production/models/task.py

class Task(models.Model):
    """任务表"""
    id = models.BigAutoField(primary_key=True)
    sheet_id = models.BigIntegerField()
    task_code = models.CharField(max_length=50)
    procedure_id = models.BigIntegerField()
    procedure_name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    completed_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=1, default='0')
    sort_order = models.IntegerField(default=0)
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'task'
```

#### JobBooking (job_booking)

```python
# apps/production/models/job_booking.py

class JobBooking(models.Model):
    """报工记录表"""
    id = models.BigAutoField(primary_key=True)
    sheet_id = models.BigIntegerField()
    task_id = models.BigIntegerField()
    procedure_id = models.BigIntegerField()
    procedure_name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    defect_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booking_time = models.DateTimeField()
    operator_id = models.BigIntegerField()
    operator_name = models.CharField(max_length=50)
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'job_booking'
```

### 4.4 Inventory Module

#### Material (material)

```python
# apps/inventory/models/material.py

class Material(models.Model):
    """物料表"""
    id = models.BigAutoField(primary_key=True)
    material_code = models.CharField(max_length=50, unique=True)
    material_name = models.CharField(max_length=100)
    material_type = models.CharField(max_length=50, null=True, blank=True)
    specification = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    safety_stock = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'material'
```

#### Supplier (purveyor_info)

```python
# apps/inventory/models/supplier.py

class Supplier(models.Model):
    """供应商表"""
    id = models.BigAutoField(primary_key=True)
    supplier_code = models.CharField(max_length=50, unique=True)
    supplier_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tenant_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'purveyor_info'
```

### 4.5 Tenant Module

#### Tenant (sys_tenant)

```python
# tenants/models.py

class Tenant(models.Model):
    """租户表"""
    id = models.BigAutoField(primary_key=True)
    tenant_id = models.CharField(max_length=20, unique=True)
    contact_name = models.CharField(max_length=20)
    contact_phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    license_no = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    domain = models.CharField(max_length=100, null=True, blank=True)
    package_id = models.BigIntegerField()
    expire_time = models.DateTimeField(null=True, blank=True)
    account_count = models.IntegerField(default=-1)
    user_count = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default='0')
    del_flag = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = 'sys_tenant'


class TenantPackage(models.Model):
    """租户套餐表"""
    id = models.BigAutoField(primary_key=True)
    package_name = models.CharField(max_length=50)
    menu_ids = models.TextField(null=True, blank=True)
    menu_check_strictly = models.BooleanField(default=True)
    status = models.CharField(max_length=1, default='0')
    del_flag = models.CharField(max_length=1, default='0')
    create_by = models.BigIntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_by = models.BigIntegerField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = 'sys_tenant_package'
```

---

## 5. Relationship Tables

### UserRole (sys_user_role)

```python
class UserRole(models.Model):
    """用户角色关联表"""
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    role_id = models.BigIntegerField()
    
    class Meta:
        db_table = 'sys_user_role'
        unique_together = ['user_id', 'role_id']
```

### UserPost (sys_user_post)

```python
class UserPost(models.Model):
    """用户岗位关联表"""
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    post_id = models.BigIntegerField()
    
    class Meta:
        db_table = 'sys_user_post'
        unique_together = ['user_id', 'post_id']
```

### RoleMenu (sys_role_menu)

```python
class RoleMenu(models.Model):
    """角色菜单关联表"""
    id = models.BigAutoField(primary_key=True)
    role_id = models.BigIntegerField()
    menu_id = models.BigIntegerField()
    
    class Meta:
        db_table = 'sys_role_menu'
        unique_together = ['role_id', 'menu_id']
```

### RoleDept (sys_role_dept)

```python
class RoleDept(models.Model):
    """角色部门关联表"""
    id = models.BigAutoField(primary_key=True)
    role_id = models.BigIntegerField()
    dept_id = models.BigIntegerField()
    
    class Meta:
        db_table = 'sys_role_dept'
        unique_together = ['role_id', 'dept_id']
```

---

## 6. Migration Script

### MySQL to PostgreSQL Data Migration

```python
# scripts/migrate_data.py

import psycopg2
import pymysql
from decimal import Decimal

def migrate_table(mysql_conn, pg_conn, table_name, model_class):
    """
    Migrate data from MySQL to PostgreSQL
    """
    mysql_cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)
    pg_cursor = pg_conn.cursor()
    
    # Get data from MySQL
    mysql_cursor.execute(f"SELECT * FROM {table_name}")
    rows = mysql_cursor.fetchall()
    
    if not rows:
        return 0
    
    # Get column names
    columns = list(rows[0].keys())
    
    # Prepare insert statement
    placeholders = ', '.join(['%s'] * len(columns))
    column_names = ', '.join(columns)
    insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    
    # Convert and insert data
    converted_rows = []
    for row in rows:
        converted_row = []
        for value in row.values():
            if isinstance(value, Decimal):
                converted_row.append(float(value))
            else:
                converted_row.append(value)
        converted_rows.append(tuple(converted_row))
    
    pg_cursor.executemany(insert_sql, converted_rows)
    pg_conn.commit()
    
    return len(rows)


def main():
    # Connect to MySQL
    mysql_conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='cp_mes',
        charset='utf8mb4'
    )
    
    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='password',
        database='cp_mes'
    )
    
    # Tables to migrate (in order of dependencies)
    tables = [
        ('sys_tenant_package', TenantPackage),
        ('sys_tenant', Tenant),
        ('sys_dept', Dept),
        ('sys_menu', Menu),
        ('sys_post', Post),
        ('sys_role', Role),
        ('sys_user', User),
        ('sys_user_role', UserRole),
        ('sys_user_post', UserPost),
        ('sys_role_menu', RoleMenu),
        ('sys_role_dept', RoleDept),
        ('sys_dict_type', DictType),
        ('sys_dict_data', DictData),
        ('sys_config', Config),
        ('client', Client),
        ('product', Product),
        ('procedure_info', Procedure),
        ('process_route', ProcessRoute),
        ('defect', Defect),
        ('material', Material),
        ('purveyor_info', Supplier),
        ('sheet', Sheet),
        ('task', Task),
        ('job_booking', JobBooking),
    ]
    
    for table_name, model_class in tables:
        count = migrate_table(mysql_conn, pg_conn, table_name, model_class)
        print(f"Migrated {count} rows from {table_name}")
    
    mysql_conn.close()
    pg_conn.close()
    
    print("Migration completed!")


if __name__ == '__main__':
    main()
```

---

## 7. PostgreSQL Schema Creation

```sql
-- Create database
CREATE DATABASE cp_mes WITH ENCODING 'UTF8';

-- Connect to database
\c cp_mes

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schemas for multi-tenancy
CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS tenant_001;
CREATE SCHEMA IF NOT EXISTS tenant_002;

-- Set search path
SET search_path TO public;
```

---

## 8. Index Creation

```sql
-- User indexes
CREATE INDEX idx_user_dept ON sys_user(dept_id);
CREATE INDEX idx_user_status ON sys_user(status);
CREATE INDEX idx_user_tenant ON sys_user(tenant_id);

-- Role indexes
CREATE INDEX idx_role_status ON sys_role(status);
CREATE INDEX idx_role_tenant ON sys_role(tenant_id);

-- Menu indexes
CREATE INDEX idx_menu_parent ON sys_menu(parent_id);

-- Dept indexes
CREATE INDEX idx_dept_parent ON sys_dept(parent_id);
CREATE INDEX idx_dept_tenant ON sys_dept(tenant_id);

-- Sheet indexes
CREATE INDEX idx_sheet_product ON sheet(product_id);
CREATE INDEX idx_sheet_status ON sheet(status);
CREATE INDEX idx_sheet_tenant ON sheet(tenant_id);

-- Task indexes
CREATE INDEX idx_task_sheet ON task(sheet_id);
CREATE INDEX idx_task_procedure ON task(procedure_id);

-- Job booking indexes
CREATE INDEX idx_job_booking_sheet ON job_booking(sheet_id);
CREATE INDEX idx_job_booking_task ON job_booking(task_id);
CREATE INDEX idx_job_booking_time ON job_booking(booking_time);

-- Oper log indexes
CREATE INDEX idx_oper_log_time ON sys_oper_log(oper_time);
CREATE INDEX idx_oper_log_tenant ON sys_oper_log(tenant_id);

-- Login log indexes
CREATE INDEX idx_login_log_time ON sys_logininfor(login_time);
CREATE INDEX idx_login_log_tenant ON sys_logininfor(tenant_id);
```
