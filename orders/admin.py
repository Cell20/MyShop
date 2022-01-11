from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
import zipfile
import io


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def zipfiles(files):
    with zipfile.ZipFile('orders.zip', 'w') as zipObj:
        for file in files:
            zipObj.write(file)


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta   # opts = options
    output = io.BytesIO()

    # files = []
    # content_disposition = []
    # for order in queryset:
    #     filename = f'OrderID: {order.id}.csv'
    #     cd = f'attachment; filename={filename}'
    #     files.append(filename)
    #     content_disposition.append(cd)

    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')

    if len(queryset) > 1:
        content_disposition = f'attachment; filename={opts.verbose_name}.csv.zip'
        response = HttpResponse(content_type='application/zip')

    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many
              and not field.one_to_many]
    # Write a first row with header information including field names
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    if len(queryset) > 1:
        # Append individual csvs to this zip
        z = zipfile.ZipFile(response, 'w')
        z.writestr(f"anyone.csv", output.getvalue())
    return response


export_to_csv.short_description = 'Export to CSV'   # customizing name


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    # An inline allows you to include a model on the same edit page as its related model.
    # It means that Order & OrderItem models of models.py file are displayed on the same page rather than on two different pages.
    actions = [export_to_csv]
