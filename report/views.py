from django.shortcuts import render
from django.http import HttpResponse

from .DBHelper import DBHelper

# Create your views here.
def index(request):
    return render(request, 'index.html')

def ReportListAllInvoices(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT i.invoice_no as "Invoice No", i.invoice_date as "Date" '
                            ' , i.customer_code as "Customer Code", c.customer_name as "Customer Name" '
                            ' , i.due_date as "Due Date", i.total as "Total", i.vat as "VAT", i.amount_due as "Amount Due" '
                            ' , ili.product_code as "Product Code", p.name as "Product Name" '
                            ' , ili.quantity as "Quantity", ili.unit_price as "Unit Price", ili.product_total as "Extended Price" '
                            ' FROM invoice i JOIN customer c ON i.customer_code = c.customer_code '
                            '  JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                            '  JOIN product p ON ili.product_code = p.code '
                            ' ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_list_all_invoices.html', data_report)

def ReportProductsSold(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT p.code as "Code", ili.product_code as "Product Code", p.name as "Product Name" '
                            ' , SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.product_total) as "Total Value Sold" '
                            ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                            '   JOIN product p ON ili.product_code = p.code '
                            ' GROUP BY p.code, ili.product_code, p.name ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_products_sold.html', data_report)

def ReportListAllProducts(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT code as "Code", name as "Name", units as "Units" FROM product ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_list_all_products.html', data_report)

def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result

def ReportListAllReceipts(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT r.receipt_no as "Receipt No",r.receipt_date as "Receipt Date", r.customer_code as "Customer Code",c.customer_name as "Customer Name" '
                                ', r.payment_method as "Payment Name",r.total_receipt As "Total Received",r.payment_reference as "Payment Reference" '
                                ', r.remarks as "Remark", i.invoice_no AS "Invoice No",i.invoice_date AS "Invoice Date",i.amount_due AS "Invoice Full Amount" '
                                ', rli.amount_paid_here AS "Amount Paid Here" '
                                'FROM receipt r  '
                                        'JOIN customer c ON c.customer_code = r.customer_code '
                                        'JOIN receipt_line_item rli ON rli.receipt_no = r.receipt_no '
                                        'JOIN invoice i ON i.invoice_no = rli.invoice_no; ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_list_all_receipts.html', data_report)


def ReportUnpaidInvoices(request):
    db = DBHelper()
    data, columns = db.fetch ('select i.invoice_no AS "Invoice Number" , i.invoice_date AS "Date" , i.customer_code AS "Customer Code", c.customer_name AS "Customer Name" , i.amount_due AS "Amount Due" , '
                                'sum(rli.amount_paid_here) AS "Amount Paid Here" , (i.amount_due - sum(rli.amount_paid_here)) As "Amount Unpaid" '
                                ' FROM receipt r JOIN receipt_line_item rli ON rli.receipt_no = r.receipt_no '
                                'JOIN invoice i ON i.invoice_no = rli.invoice_no '
                                'JOIN customer c ON c.customer_code = i.customer_code '
                                'Group by i.invoice_no, c.customer_name , i.amount_due; ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_unpaid_invoices.html', data_report)


def ReportGroupBy(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT r.receipt_no as "Receipt No",r.receipt_date as "Receipt Date", r.customer_code as "Customer Code",c.customer_name as "Customer Name" '
                                ', r.payment_method as "Payment Name",r.total_receipt As "Total Received",r.payment_reference as "Payment Reference" '
                                ', r.remarks as "Remark", i.invoice_no AS "Invoice No",i.invoice_date AS "Invoice Date",i.amount_due AS "Invoice Full Amount" '
                                ', rli.amount_paid_here AS "Amount Paid Here" '
                                'FROM receipt r  '
                                        'JOIN customer c ON c.customer_code = r.customer_code '
                                        'JOIN receipt_line_item rli ON rli.receipt_no = r.receipt_no '
                                        'JOIN invoice i ON i.invoice_no = rli.invoice_no; ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_group_by.html', data_report)


