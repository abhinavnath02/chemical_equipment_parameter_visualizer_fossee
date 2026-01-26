from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import Dataset
from .utils import analyze_csv
from .pdf_generator import generate_pdf_report

class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            summary = analyze_csv(file)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        dataset = Dataset.objects.create(
            filename=file.name,
            total_equipment=summary["total_equipment"],
            avg_flowrate=summary["avg_flowrate"],
            avg_pressure=summary["avg_pressure"],
            avg_temperature=summary["avg_temperature"]
        )

        # keep only last 5
        if Dataset.objects.count() > 5:
            oldest = Dataset.objects.order_by('uploaded_at').first()
            if oldest:
                oldest.delete()

        return Response(summary, status=201)

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        datasets = Dataset.objects.order_by('-uploaded_at')[:5]
        data = [
            {
                "filename": d.filename,
                "uploaded_at": d.uploaded_at,
                "total_equipment": d.total_equipment
            }
            for d in datasets
        ]
        return Response(data)

class GeneratePDFView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        
        if not data:
            return Response({"error": "No data provided"}, status=400)
        
        try:
            pdf_buffer = generate_pdf_report(data)
            
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="equipment_report_{data.get("total_equipment", "")}_items.pdf"'
            
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=500)
