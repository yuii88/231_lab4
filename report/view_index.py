
from report.models import *

def index(request):
    invoice_no = request.GET.get('inv','')
    data_report = dict()
    data_report['invoice'] = list(Invoice.objects.filter(invoice_no=invoice_no).select_related('customer_code').values('invoice_no', 'date', 'customer_code_id', 'customer_code__name','due_date','total','vat','amount_due'))
    data_report['invoice_line_item'] = list(InvoiceLineItem.objects.filter(invoice_no=invoice_no).values())
    #return JsonResponse(data_report)
    return render(request, 'report_data.html', data_report)