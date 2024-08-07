import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UploadedFile, OutputData
from .forms import UploadFileForm
from django.conf import settings
import os
from datetime import datetime
import datetime


def UploadedExcel(f):
    output_data = []
    masterfile = pd.read_excel(os.path.join(settings.BASE_DIR, 'report', 'master.xlsx'))
    xls = pd.ExcelFile(f)

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        print(f"Sheet: {sheet_name}")
        print("Columns in DataFrame:", df.columns)
        num_columns = len(df.columns)
        new_column_names = [f'Column_{i}' for i in range(num_columns)]
        df.columns = new_column_names
        for index, row in df.iterrows():
            if 'Previous Year' in row.values:
                if index > 0:

                    previous_row_name = df.iloc[index - 1, 0]
                    df.iloc[index, 0] = previous_row_name

        print("New Column Names:", df.columns)
        if sheet_name in ["Health Portfolio", "Liability Portfolio"]:
            row_index = 1
        else:
            row_index = 0
        if not df.empty and df.shape[0] > row_index:

            row_values = df.iloc[row_index].dropna().tolist()
            print(row_values)

            ZipFile = df.merge(masterfile, left_on='Column_0', right_on='insurer')
            print(ZipFile)
            for _, row in ZipFile.iterrows():

                for product_name, p in zip(new_column_names[1:], row_values):
                    value = row.get(product_name, None)

                    if value is None or pd.isna(value):
                        continue

                    output_row = OutputData(
                        year=datetime.date.today().year - 1,
                        month="Dec",
                        clubbed_name=row['clubbed_name'],
                        product=p,
                        value=row[product_name]
                    )
                    output_row.save()

            for index, row in ZipFile.iterrows():
                if index % 2 == 0:
                    year = datetime.date.today().year
                else:
                    year = datetime.date.today().year - 1

                for product_name, p in zip(new_column_names[1:], row_values):
                    output_row1 = {
                        'year': year,
                        'month': 'Dec',
                        'clubbed_name': row.get('clubbed_name', 'Unknown'),
                        'product': p,
                        'value': row.get(product_name, 0)
                    }
                    output_data.append(output_row1)


    OutputFile = pd.DataFrame(output_data)
    OutputFile = OutputFile.sort_values(by='clubbed_name')
    OutputFile = OutputFile.sort_values(by='year', ascending=False)
    OutputFile = OutputFile.fillna(0)
    timeinfo = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    outputfilename = f'output_{timeinfo}.xlsx'
    plotfilename = f'plot_{timeinfo}.png'
    outputfilepath = os.path.join(settings.MEDIA_ROOT, outputfilename)
    plotfilepath = os.path.join(settings.MEDIA_ROOT, plotfilename)

    OutputFile.to_excel(outputfilepath, index=False)


    OutputFile.groupby('product').sum()['value'].plot(kind='bar', color='Blue')
    plt.figure(figsize=(10, 6))
    OutputFile.groupby('product').sum()['value'].plot(kind='bar', color='Blue')
    plt.title('PLOTS ACCORDING TO VALUE', fontsize=10)
    plt.xlabel('Product', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout(pad=2.0)
    plt.savefig(plotfilepath)

    return outputfilepath, plotfilepath

def FileUpload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            outputfilepath, plotfilepath = UploadedExcel(request.FILES['file'])
            output_url = request.build_absolute_uri(f'/media/{os.path.basename(outputfilepath)}')
            plot_url = request.build_absolute_uri(f'/media/{os.path.basename(plotfilepath)}')
            return render(request, 'upload/upload.html', {'output_file':   output_url , 'plot':plot_url })
    else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})


def DownloadFile(request):
    file_name = 'output.xlsx'  # Change to your file name
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)


    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

def ShowPlot(request, plotfilepath):
    with open(plotfilepath, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')






