from typing import Dict, List
from app.services.report.pdf_report import PDFReportGenerator

class ReportBuilderService:
    """
    Builder service for constructing digital assessment reports.
    """
    @staticmethod
    def build_report(
        grading_result: Dict,
        classifications: List[Dict],
        annotated_image_url: str,
        upload_id: str
    ) -> Dict:
        pdf_url = PDFReportGenerator.generate_pdf(
            grading_data=grading_result,
            classifications=classifications,
            annotated_image_url=annotated_image_url,
            upload_id=upload_id
        )

        return {
            "batch_id": grading_result["batch_id"],
            "upload_id": upload_id,
            "timestamp": grading_result["timestamp"],
            "pdf_report_url": pdf_url,
            "status": "success"
        }
