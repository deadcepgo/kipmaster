from django.contrib import admin

from models import Item,Treb,Tag,LocalObject,Files,CommentItem,Phone,PhoneCat,Journal,TOBlank,TOMonth, Task
#from reversion.admin import VersionAdmin
from mptt.admin import MPTTModelAdmin

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name','mark','model','serial','date_pov','date_cal','date_mk','par','active','dattype')
	list_filter = ('active','date_pub','date_edit','lobject')
	search_fields = ['name']
	list_editable = ('serial',)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name')
class PhoneAdmin(admin.ModelAdmin):
	list_display = ('name','num','is_ration')
class TOBAdmin(admin.ModelAdmin):
	list_display = ('name','label')
class TMAdmin(admin.ModelAdmin):
	list_display = ('name','label','parent','get_childs')
class TaskAdm(admin.ModelAdmin):
	list_display = ('date_pub','date_up','date_end','date_deadline','user','status')
admin.site.register(Item,ItemAdmin)
admin.site.register(Tag)
admin.site.register(LocalObject,MPTTModelAdmin)
admin.site.register(Files)
admin.site.register(CommentItem)
admin.site.register(Phone,PhoneAdmin)
admin.site.register(PhoneCat)
admin.site.register(Journal)
admin.site.register(TOBlank,TOBAdmin)
admin.site.register(TOMonth,TMAdmin)
admin.site.register(Task,TaskAdm)
admin.site.register(Treb)
#@admin.register(CommentItem)
#class CommentVersion(VersionAdmin):
#	pass
