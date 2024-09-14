from django.http import JsonResponse
from loganalyzer.util_funcs_log import scan_logs_for_unique

def count_logs(request, date_string):
    result = scan_logs_for_unique(date_string)
    
    if result['error']:
        return JsonResponse({'error': result['error']}, status=400)
    
    return JsonResponse({'count': result['count']})
