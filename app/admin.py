from django.contrib import admin


from .models import Person,Course,UandC,UandP,CandImg
# Register your models here.
admin.site.site_header = 'kks'  # 设置header
admin.site.site_title = 'kks'   # 设置title
admin.site.index_title = 'kks'
admin.site.register(Person)
admin.site.register(Course)
admin.site.register(UandC)
admin.site.register(UandP)
admin.site.register(CandImg)
