"""
Report views for cp_mes project.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta, datetime

from apps.core.permissions import IsAuthenticated
from apps.production.models import Sheet, Task, JobBooking
from apps.basic_data.models import Product, Defect


class ProductionStatisticsView(APIView):
    """
    Production statistics view.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get production statistics.
        """
        # Get date range
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')
        
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            # Default to last 30 days
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
        
        # Get job bookings in date range
        job_bookings = JobBooking.objects.filter(
            booking_time__date__range=[start_date.date(), end_date.date()]
        )
        
        # Calculate statistics
        total_production = job_bookings.aggregate(
            total=Sum('quantity')
        )['total'] or 0
        
        total_defect = job_bookings.aggregate(
            total=Sum('defect_quantity')
        )['total'] or 0
        
        quality_rate = ((total_production - total_defect) / total_production * 100) if total_production > 0 else 100
        
        # Get sheet statistics
        sheets = Sheet.objects.filter(
            create_time__date__range=[start_date.date(), end_date.date()]
        )
        
        sheet_stats = sheets.values('status').annotate(
            count=Count('id')
        )
        
        return Response({
            'code': 200,
            'msg': '获取成功',
            'data': {
                'totalProduction': float(total_production),
                'totalDefect': float(total_defect),
                'qualityRate': round(quality_rate, 2),
                'jobBookingCount': job_bookings.count(),
                'sheetStats': list(sheet_stats),
                'dateRange': {
                    'startDate': start_date.strftime('%Y-%m-%d'),
                    'endDate': end_date.strftime('%Y-%m-%d'),
                }
            }
        })


class DefectAnalysisView(APIView):
    """
    Defect analysis view.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get defect analysis.
        """
        # Get date range
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')
        
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
        
        # Get job bookings with defects
        job_bookings = JobBooking.objects.filter(
            booking_time__date__range=[start_date.date(), end_date.date()],
            defect_quantity__gt=0
        )
        
        # Analyze defect details
        defect_stats = {}
        for jb in job_bookings:
            if jb.defect_details:
                for detail in jb.defect_details:
                    defect_name = detail.get('defect_name', 'Unknown')
                    quantity = detail.get('quantity', 0)
                    if defect_name not in defect_stats:
                        defect_stats[defect_name] = 0
                    defect_stats[defect_name] += quantity
        
        # Sort by quantity
        sorted_defects = sorted(
            defect_stats.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return Response({
            'code': 200,
            'msg': '获取成功',
            'data': {
                'defectStats': [{'name': k, 'quantity': v} for k, v in sorted_defects],
                'totalDefect': sum(defect_stats.values()),
                'defectCount': len(defect_stats),
            }
        })


class ProductOutputView(APIView):
    """
    Product output view.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get product output statistics.
        """
        # Get date range
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')
        
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
        
        # Get job bookings grouped by product
        job_bookings = JobBooking.objects.filter(
            booking_time__date__range=[start_date.date(), end_date.date()]
        ).values('sheet__product_id', 'sheet__product_name').annotate(
            total_quantity=Sum('quantity'),
            total_defect=Sum('defect_quantity'),
            booking_count=Count('id')
        )
        
        return Response({
            'code': 200,
            'msg': '获取成功',
            'data': list(job_bookings)
        })


class DailyTrendView(APIView):
    """
    Daily production trend view.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get daily production trend.
        """
        # Get date range
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Get daily statistics
        daily_stats = []
        current_date = start_date
        while current_date <= end_date:
            job_bookings = JobBooking.objects.filter(
                booking_time__date=current_date
            )
            
            total_quantity = job_bookings.aggregate(
                total=Sum('quantity')
            )['total'] or 0
            
            total_defect = job_bookings.aggregate(
                total=Sum('defect_quantity')
            )['total'] or 0
            
            daily_stats.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'production': float(total_quantity),
                'defect': float(total_defect),
            })
            
            current_date += timedelta(days=1)
        
        return Response({
            'code': 200,
            'msg': '获取成功',
            'data': daily_stats
        })
