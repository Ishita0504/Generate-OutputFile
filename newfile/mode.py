from upload.models import UploadedFile, OutputData

# Fetch all records from UploadedFile
uploaded_files = UploadedFile.objects.all()
print(uploaded_files)

# Fetch all records from OutputData
output_data = OutputData.objects.all()
print(output_data)
uploaded_files = UploadedFile.objects.all()
for file in uploaded_files:
    print(file)

# Check all records in OutputData
output_data = OutputData.objects.all()
for data in output_data:
    print(data)
