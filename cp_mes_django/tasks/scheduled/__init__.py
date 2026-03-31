"""
Scheduled Celery tasks for cp_mes project.
"""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def clean_expired_sessions():
    """
    Clean expired sessions from database.
    """
    try:
        from django.contrib.sessions.models import Session
        expired_count = Session.objects.filter(
            expire_date__lt=timezone.now()
        ).delete()[0]
        logger.info(f"Cleaned {expired_count} expired sessions")
        return expired_count
    except Exception as e:
        logger.error(f"Error cleaning sessions: {e}")
        return 0


@shared_task
def clean_old_logs():
    """
    Clean old operation and login logs (older than 30 days).
    """
    try:
        from apps.system.models import OperLog, LoginLog
        
        threshold = timezone.now() - timedelta(days=30)
        
        oper_log_count = OperLog.objects.filter(
            oper_time__lt=threshold
        ).delete()[0]
        
        login_log_count = LoginLog.objects.filter(
            login_time__lt=threshold
        ).delete()[0]
        
        logger.info(f"Cleaned {oper_log_count} operation logs and {login_log_count} login logs")
        return oper_log_count + login_log_count
    except Exception as e:
        logger.error(f"Error cleaning logs: {e}")
        return 0


@shared_task
def generate_daily_report():
    """
    Generate daily production report.
    """
    try:
        from apps.production.models import Sheet, JobBooking
        from datetime import date
        
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        # Get yesterday's statistics
        sheets = Sheet.objects.filter(
            create_time__date=yesterday
        )
        
        job_bookings = JobBooking.objects.filter(
            booking_time__date=yesterday
        )
        
        total_quantity = sum(jb.quantity for jb in job_bookings)
        total_defect = sum(jb.defect_quantity for jb in job_bookings)
        
        report_data = {
            'date': str(yesterday),
            'new_sheets': sheets.count(),
            'total_production': float(total_quantity),
            'total_defect': float(total_defect),
            'quality_rate': float((total_quantity - total_defect) / total_quantity * 100) if total_quantity > 0 else 100,
        }
        
        logger.info(f"Daily report generated: {report_data}")
        return report_data
    except Exception as e:
        logger.error(f"Error generating daily report: {e}")
        return None


@shared_task
def check_low_stock():
    """
    Check for materials with low stock and send alerts.
    """
    try:
        from apps.inventory.models import Material
        
        low_stock_materials = [m for m in Material.objects.filter(status='0') if m.is_low_stock]
        
        if low_stock_materials:
            logger.warning(f"Found {len(low_stock_materials)} materials with low stock")
            for material in low_stock_materials:
                logger.warning(
                    f"Low stock alert: {material.material_name} "
                    f"(current: {material.quantity}, safety: {material.safety_stock})"
                )
        
        return len(low_stock_materials)
    except Exception as e:
        logger.error(f"Error checking low stock: {e}")
        return 0


@shared_task
def update_sheet_status():
    """
    Update sheet status based on completion.
    """
    try:
        from apps.production.models import Sheet
        
        # Find sheets that should be completed
        sheets_to_complete = Sheet.objects.filter(
            status='1',  # In progress
            completed_quantity__gte=models.F('quantity')
        )
        
        count = 0
        for sheet in sheets_to_complete:
            sheet.complete_production()
            count += 1
        
        logger.info(f"Updated {count} sheets to completed status")
        return count
    except Exception as e:
        logger.error(f"Error updating sheet status: {e}")
        return 0


@shared_task
def send_notification(user_id, title, message):
    """
    Send notification to user.
    """
    try:
        # TODO: Implement notification sending (email, SMS, push, etc.)
        logger.info(f"Notification sent to user {user_id}: {title}")
        return True
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        return False
