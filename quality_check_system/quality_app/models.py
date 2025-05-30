from django.db import models

# Create your models here.
class Defect(models.Model):
    # 원본 파일 절대 경로
    image_path = models.TextField(blank=True, null=True)
    # 웹에서 접근 가능한 이미지 URL
    web_image_url = models.TextField(blank=True, null=True)

    defect_type = models.TextField(blank=True, null=True)
    current_saturation = models.FloatField(blank=True, null=True)
    reference_saturation = models.FloatField(blank=True, null=True)
    tolerance = models.FloatField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'defects_table'
        managed = False # Consumer 스크립트가 직접 테이블 생성하고 관리
        ordering = ['-timestamp'] # 최신 기록부터 정렬

    def __str__(self):
        return f"Defect {self.id} ({self.defect_type}) at {self.timestamp}"
    
