"""
Department model for cp_mes project.
Maps to sys_dept table.
"""

from django.db import models


class Dept(models.Model):
    """
    Department model.
    Maps to sys_dept table.
    """
    
    id = models.BigAutoField(primary_key=True)
    parent_id = models.BigIntegerField(default=0, verbose_name='父部门ID')
    ancestors = models.CharField(max_length=50, default='', verbose_name='祖级列表')
    dept_name = models.CharField(max_length=30, verbose_name='部门名称')
    order_num = models.IntegerField(default=0, verbose_name='显示顺序')
    leader = models.CharField(max_length=20, null=True, blank=True, verbose_name='负责人')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='联系电话')
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name='邮箱')
    status = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='部门状态'
    )  # 0=正常, 1=停用
    del_flag = models.CharField(
        max_length=1, 
        default='0',
        verbose_name='删除标志'
    )  # 0=存在, 2=删除
    
    # Multi-tenant
    tenant_id = models.BigIntegerField(null=True, blank=True, verbose_name='租户ID')
    
    # Audit fields
    create_by = models.BigIntegerField(null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_by = models.BigIntegerField(null=True, blank=True, verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'sys_dept'
        verbose_name = '部门'
        verbose_name_plural = '部门'
        ordering = ['order_num']
    
    def __str__(self):
        return self.dept_name
    
    @property
    def is_active(self):
        return self.status == '0' and self.del_flag == '0'
    
    def get_children(self):
        return Dept.objects.filter(parent_id=self.id, del_flag='0')
    
    def get_all_children_ids(self):
        """
        Get all descendant department IDs.
        """
        result = [self.id]
        children = self.get_children()
        for child in children:
            result.extend(child.get_all_children_ids())
        return result
    
    @classmethod
    def get_tree(cls, parent_id=0):
        """
        Get department tree structure.
        """
        depts = cls.objects.filter(parent_id=parent_id, del_flag='0').order_by('order_num')
        result = []
        for dept in depts:
            item = {
                'id': dept.id,
                'deptName': dept.dept_name,
                'parentId': dept.parent_id,
                'orderNum': dept.order_num,
                'leader': dept.leader,
                'phone': dept.phone,
                'email': dept.email,
                'status': dept.status,
            }
            children = dept.get_children()
            if children.exists():
                item['children'] = cls.get_tree(dept.id)
            result.append(item)
        return result
