"""
Menu model for cp_mes project.
Maps to sys_menu table.
"""

from django.db import models


class Menu(models.Model):
    """
    Menu model.
    Maps to sys_menu table.
    """
    
    id = models.BigAutoField(primary_key=True)
    menu_name = models.CharField(max_length=50, verbose_name='菜单名称')
    parent_id = models.BigIntegerField(default=0, verbose_name='父菜单ID')
    order_num = models.IntegerField(default=0, verbose_name='显示顺序')
    path = models.CharField(max_length=200, null=True, blank=True, verbose_name='路由地址')
    component = models.CharField(max_length=255, null=True, blank=True, verbose_name='组件路径')
    query = models.CharField(max_length=255, null=True, blank=True, verbose_name='路由参数')
    route_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='路由名称')
    is_frame = models.CharField(
        max_length=1, 
        default='1',
        verbose_name='是否为外链'
    )  # 0=是, 1=否
    is_cache = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='是否缓存'
    )  # 0=缓存, 1=不缓存
    menu_type = models.CharField(
        max_length=1, 
        default='M',
        verbose_name='菜单类型'
    )  # M=目录, C=菜单, F=按钮
    visible = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='菜单状态'
    )  # 0=显示, 1=隐藏
    status = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='菜单状态'
    )  # 0=正常, 1=停用
    perms = models.CharField(max_length=100, null=True, blank=True, verbose_name='权限标识')
    icon = models.CharField(max_length=100, default='#', verbose_name='菜单图标')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'sys_menu'
        verbose_name = '菜单'
        verbose_name_plural = '菜单'
        ordering = ['order_num']
    
    def __str__(self):
        return self.menu_name
    
    @property
    def is_catalog(self):
        return self.menu_type == 'M'
    
    @property
    def is_menu(self):
        return self.menu_type == 'C'
    
    @property
    def is_button(self):
        return self.menu_type == 'F'
    
    @property
    def is_visible(self):
        return self.visible == '0'
    
    @property
    def is_active(self):
        return self.status == '0'
    
    def get_children(self):
        return Menu.objects.filter(parent_id=self.id)
    
    @classmethod
    def get_tree(cls, parent_id=0):
        """
        Get menu tree structure.
        """
        menus = cls.objects.filter(parent_id=parent_id, status='0').order_by('order_num')
        result = []
        for menu in menus:
            item = {
                'id': menu.id,
                'menuName': menu.menu_name,
                'parentId': menu.parent_id,
                'orderNum': menu.order_num,
                'path': menu.path,
                'component': menu.component,
                'menuType': menu.menu_type,
                'visible': menu.visible,
                'icon': menu.icon,
                'perms': menu.perms,
            }
            children = menu.get_children()
            if children.exists():
                item['children'] = cls.get_tree(menu.id)
            result.append(item)
        return result
