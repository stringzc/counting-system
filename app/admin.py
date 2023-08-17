from django.contrib import admin


from .models import Person,Course,UandC,UandP,CandImg,QDI,DLI,BDI,UCI,plun,black,BASIC
# Register your models here.
admin.site.site_header = 'kks'  # 设置header
admin.site.site_title = 'kks'   # 设置title
admin.site.index_title = 'kks'
admin.site.register(Person)
admin.site.register(Course)
admin.site.register(UandC)
admin.site.register(UandP)
admin.site.register(CandImg)
admin.site.register(QDI)
admin.site.register(DLI)
admin.site.register(BDI)
admin.site.register(UCI)
admin.site.register(plun)
admin.site.register(black)
admin.site.register(BASIC)

