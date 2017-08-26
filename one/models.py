#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from transliterate import translit
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey,TreeManyToManyField
from django import forms
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from ckeditor_uploader.fields import RichTextUploadingField

def get_translit(string):
		s 		= translit(string,'ru', reversed=True).split()
		s 		= "-".join(s)
		return s
class Tag(models.Model):
	name		= models.CharField(max_length=30)
	def get_translit(string):
		s 		= translit(string,'ru', reversed=True).split()
		s 		= "-".join(s)
		return s
	class Meta:
		verbose_name=u'Тег'
		verbose_name_plural=u'Теги'

	
	def __unicode__(self):
		return self.name
class LocalObject(MPTTModel):
	name		= models.CharField(max_length=150,verbose_name=u'Название объекта')
	parent		= TreeForeignKey('self',null=True,blank=True,verbose_name=u'Родитель объекта',related_name='child')
	to_yan		= models.CharField(max_length=30,blank=True,null=True,verbose_name=u'номер месяца в котором ТО-3')
	to_main		= models.BooleanField(default=False,verbose_name=u'Объект ТО для ежедневных актов')
	asipaz_p	= models.CharField(max_length=30,blank=True,null=True,verbose_name=u'номер месяца в котором полная проверка АСиПАЗ')
	def get_to_num(self,mounth=None):
		to_three = int(self.to_yan)
		if mounth is None:
			mounth = int(datetime.datetime.now().month)
		if mounth == to_three:
			to = 3
		elif mounth == to_three+3 or mounth == to_three+6 or mounth == to_three+9 or mounth == to_three-3 or mounth == to_three-6 or mounth == to_three-9:
			to = 2
		else:
			to = 1
		return to
	def get_asipaz(self):
		if self.asipaz_p is not None:
			full = self.asipaz_p
			month = int(datetime.datetime.now().month)
			if month == int(full):
				asipaz = u'П'
			elif month == int(full)+3 or month == int(full)+6 or month == int(full)+9 or month == int(full)-3 or month == int(full)-6 or month == int(full)-9:
				asipaz = u'К'
			else:
				asipaz = u'none'
		else:
			asipaz = u'none'
		return asipaz
	def get_items(self):
		return Item.objects.filter(lobject=self).order_by('par_iz')
	def __unicode__(self):
		parent = self.parent
		parents = ''
		while parent:
			parents+='---'
			parent = parent.parent
		return parents+self.name
	def get_parents(self):
		parent = self.parent
		parents = []
		while parent:
			parents.append(parent)
			parent = parent.parent
		return parents
	def get_childs(self):
		childs = self.child.all()
		childs_all = []
		if len(childs)>0:
			for child in childs:
				childs_all.append(child.get_childs())
		else:
			childs_all.append(self)
		return childs_all
	class MPTTMeta:
		level_attr = 'mptt_level'
		order_insertion_by=['name']
	class Meta:
		verbose_name=u'Расположение'
		verbose_name_plural=u'Расположения'
class Item(models.Model):
	STATUS = (('act',u'В работе'),('not',u'Не в работе'),('rez',u'Резерв'))
	name 		= models.CharField(max_length=150, default='--',verbose_name=u'Наименование оборудования')
	mark 		= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Марка')
	model 		= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Модель')
	serial 		= models.CharField(max_length=300, default='--', blank=True,verbose_name=u'Серийный номер')
	date_pov 	= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Дата поверки')
	date_cal 	= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Дата калибровки')
	date_mk 	= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Дата изготовления')
	par 		= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Еденица измерения')
	active 		= models.CharField(max_length=150,default='act',choices=STATUS, blank=True,verbose_name=u'Статус')
	dattype 	= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'')
	tags 		= models.ManyToManyField(Tag , blank=True,verbose_name=u'Теги')
	lobject 	= models.ManyToManyField(LocalObject, blank=True,verbose_name=u'Расположение',related_name='items')
	ti 			= models.CharField(max_length=30, default='', blank=True,verbose_name=u'Тип измерения')
	greer 		= models.CharField(max_length=100, default='--',verbose_name=u'Гос реестр')
	min_z		= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Минимальное значение')
	max_z		= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Максимальное значение')
	sig			= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Погрешность')
	mpi			= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Межповерочный интервал')
	sr_sl		= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Срок службы')
	par_iz		= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Измеряемый параметр')
	otm_o_pov 	= models.CharField(max_length=100, default='--', blank=True,verbose_name=u'Отметка о поверке')
	date_pub	= models.DateTimeField(auto_now_add=True,blank=True,verbose_name=u'Дата публикации')
	date_edit	= models.DateTimeField(auto_now=True,blank=True,verbose_name=u'Дата изменения')
	who_edit	= models.CharField(max_length=100,default='######',verbose_name=u'Кто изменил')
	pe 			= models.BooleanField(default=True,blank=True,verbose_name=u'Заземлено?')
	bir_tr 		= models.BooleanField(default=True,blank=True,verbose_name=u'Наличие треугольной бирки')
	bir_pr 		= models.BooleanField(default=True,blank=True,verbose_name=u'Наличие прямоугольной бирки')
	def __init__(self, *args, **kwargs):
		
		super(Item,self).__init__(*args, **kwargs)
		
	def get_pov(self):
		date = self.date_pov.split('.')
		if len(date) == 3:
			day = date[0]
			month = date[1]
			year = date[2]
			return day,month,year
		elif len(date)== 2:
			month = date[0]
			year = date[1]
			return month,year
	def save(self, *args, **kwargs):
		
		#if self.was_active and self.active:
		#	Journal.objects.create(name='item_status',created=False,edited=True,meta=self.active,par_id=self.id)
		super(Item, self).save(*args, **kwargs)
		

	def __unicode__(self):
		return self.name+'_'+self.mark+'_'+self.model+'_'+str(self.id)
	class Meta:
		verbose_name=u'Прибор'
		verbose_name_plural=u'Приборы'

class Files(models.Model):
	name		= models.CharField(max_length=150, default=u'somefile',blank=True,verbose_name=u'Название файла')
	document	= models.FileField(upload_to='docs/',verbose_name=u'Файл')
	#parents		= models.ManyToManyField(Item,blank=True,verbose_name=u'Родитель файла')
	parent 		= models.CharField(default='item',max_length=30,verbose_name=u'Родитель')
	parent_id   = models.IntegerField(verbose_name=u'ID родителя',null=True)
	date_pub    = models.DateTimeField(auto_now_add=True,blank=True,verbose_name=u'Дата публикации')
	def __unicode__(self):
		return self.name
	def get_parent(self):
		if self.parent == 'lobj':
			return LocalObject.objects.get(id=int(self.parent_id))
		if self.parent == 'item':
			return Item.objects.get(id=int(self.parent_id))
		if self.parent == 'comment':
			return Item.objects.get(id=int(self.parent_id))
		if self.parent == 'task':
			return Task.objects.get(id=int(self.parent_id))
	class Meta:
		verbose_name=u'Файл'
		verbose_name_plural=u'Файлы'
class CommentItem(models.Model):
	user = models.CharField(max_length=30,verbose_name=u'Пользователь')
	text =RichTextUploadingField(verbose_name=u'Текст')
	date_pub = models.DateTimeField(auto_now_add=True,blank=True,verbose_name=u'Дата публикации')
	#file = models.ForeignKey(Files,blank=True,default='',null=True,verbose_name=u'Файл')
	par = models.CharField(max_length=30,default='item',verbose_name=u'Родитель')
	par_id = models.CharField(max_length=30,default='',verbose_name=u'ID Родителя')
	def __unicode__(self):
		if len(self.text)>30:
			return self.text[0:30]+'...'
		else:
			return self.text
	class Meta:
		verbose_name=u'Коментарий'
		verbose_name_plural=u'Коментарии'
	def get_parent(self):
		if self.par == 'item':
			return Item.objects.get(id=int(self.par_id))
		if self.par == 'lobject':
			return LocalObject.objects.get(id=int(self.par_id))
		if self.par == 'task':
			return Task.objects.get(id=int(self.par_id))
class PhoneCat(MPTTModel):
	name = models.CharField(max_length=50,verbose_name=u'Название')
	parent = TreeForeignKey('self',null=True,blank=True,verbose_name=u'Родитель')
	class MPTTMeta:
		level_attr = 'mptt_level'
	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name=u'Телефонная категория'
		verbose_name_plural=u'Телефонные категории'

class Phone(models.Model):
	name = models.CharField(max_length=50,verbose_name=u'Имя')
	num = models.CharField(max_length=20,verbose_name=u'Номер')
	is_ration = models.BooleanField(default=False,verbose_name=u'Рация?')
	cat = models.ForeignKey(PhoneCat,verbose_name=u'Категория')
	def __unicode__(self):
		return self.name+' : '+self.num
	class Meta:
		verbose_name=u'Телефон'
		verbose_name_plural=u'Телефоны'
class Journal(models.Model):
	name = models.CharField(max_length=100,blank=True,default='')
	created = models.BooleanField(default=False,verbose_name=u'Добавлено?')
	edited = models.BooleanField(default=True,verbose_name=u'Изменено?')
	time = models.DateTimeField(auto_now_add=True,blank=True,verbose_name=u'Время события')
	meta = models.CharField(max_length=200,blank=True,default='',verbose_name=u'Дополнительная информация')
	par_id = models.CharField(max_length=4,verbose_name=u'Родитель')
	parent = models.CharField(max_length=100,default='',verbose_name=u'Родитель')
	def __unicode__(self):
		return self.name+'---'+str(self.time)
	class Meta:
		verbose_name=u'Журнал'
		verbose_name_plural=u'Журналы'
	def get_byid(self):
		if self.parent == 'item':
			return Item.objects.get(id=int(self.par_id))
		elif self.parent == 'comment':
			return CommentItem.objects.get(id=int(self.par_id))
		elif self.parent == 'file':
			return Files.objects.get(id=int(self.par_id))
		elif self.parent == 'tob':
			return TOBlank.objects.get(id=int(self.par_id))
		elif self.parent == 'tom':
			return TOMonth.objects.get(id=int(self.par_id))
		elif self.parent == 'phone':
			return Phone.objects.get(id=int(self.par_id))
		elif self.parent == 'phc':
			return PhoneCat.objects.get(id=int(self.par_id))
		elif self.parent == 'lobj':
			return LocalObject.objects.get(id=int(self.par_id))
		elif self.parent == 'task':
			return Task.objects.get(id=int(self.par_id))
		else:
			return 'none'

class TOBlank(models.Model):
	name = models.CharField(max_length=100,verbose_name=u'Название объекта ТО')
	label = models.CharField(max_length=100,verbose_name=u'Ярлык(например УПСВ-1)')
	childs = models.ManyToManyField(LocalObject,blank=True,verbose_name=u'Объекты на ТО(например н/а№2)')
	dmn = models.IntegerField(blank=True,default=1,verbose_name=u'День начала проведения ТО')
	dme = models.IntegerField(blank=True,default=1,verbose_name=u'День окончания проведения ТО')

	def __unicode__(self):
		return self.label
	class Meta:
		verbose_name=u'Бланк ТО'
		verbose_name_plural=u'Бланки ТО'
class TOMonth(MPTTModel):
	name = models.CharField(max_length=200,verbose_name=u'Название')
	label = models.CharField(max_length=200,verbose_name=u'Ярлык')
	parent = TreeForeignKey('self',blank=True,null=True,verbose_name=u'Родитель',related_name='child')
	childs = models.ManyToManyField(LocalObject,blank=True,verbose_name=u'Объекты')
	kip = models.BooleanField(default=False,blank=True,verbose_name=u'Оборудование КИП?')
	asu = models.BooleanField(default=False,blank=True,verbose_name=u'Оборудование АСУ?')
	status = models.BooleanField(default=True,blank=True,verbose_name=u'В работе?')
	prim = models.CharField(max_length=200,blank=True,default='',verbose_name=u'Примечание')
	def __unicode__(self):
		return self.name
	def get_childs(self):
		s = ''
		for child in self.childs.all():
			s+=child.name+', '
		return s
	def get_asipaz_obj(self):
		s=[]
		childs=self.child.all()
		if len(childs)>0:
			for child in childs:
				sub_childs = child.childs.all()
				if len(sub_childs)>0:
					for sub_child in sub_childs:
						if sub_child.get_asipaz() != 'none':
							s.append(sub_child)
		return s
class Task(models.Model):
	STATUS = (('act',u'В работе'),('wai',u'Ожидание'),('end',u'Выполнено'))
	date_pub = models.DateTimeField(auto_now_add=True,blank=True,verbose_name=u'Дата публикации')
	date_up = models.DateTimeField(auto_now=True,blank=True,verbose_name=u'Дата обновления')
	date_end = models.DateTimeField(blank=True,null=True,verbose_name=u'Дата окончания')
	date_deadline = models.DateTimeField(blank=True,null=True,verbose_name=u'Крайний срок')
	date_on = models.DateField(blank=True,null=True,verbose_name=u'Дата мероприятия')
	text = RichTextUploadingField(verbose_name=u'Текст задачи')
	user = models.CharField(blank=True,default='none',max_length=200,verbose_name=u'Имя пользователя')
	status = models.CharField(default='act',choices=STATUS,blank=True,max_length=200,verbose_name=u'Статус')
	lobj = models.ForeignKey(LocalObject,blank=True,null=True,verbose_name=u'Объект')
	def __unicode__(self):
		return str(self.date_pub)+' | '+self.status+' | '+self.text[:50]
	class Meta:
		verbose_name=u'Задача'
		verbose_name_plural=u'Задачи'
class Treb(models.Model):
	name 	= models.CharField(max_length=300,verbose_name=u'Наименование')
	obj 	= models.ManyToManyField(LocalObject,blank=True,null=True,verbose_name=u'Объект')
	item 	= models.ForeignKey(Item,blank=True,null=True,verbose_name=u'Прибор')
	col 	= models.IntegerField(blank=True,verbose_name=u'Количество')
	def __unicode__(self):
		return self.name

#class Graphic(models.Model):
#	full name
#	dol


#################################FORMS#######################################
class UploadFileForm(forms.ModelForm):
	
	class Meta:
		model = Files
		fields = '__all__'
class AddItem(forms.ModelForm):
	class Meta:
		model = Item
		fields = '__all__'
###############################SIGNALS##########################################
@receiver(post_save,sender=Item)
def added_item_c(sender,instance,created,update_fields,raw,**kwargs):
	if created:
		Journal.objects.create(parent='item',created=True,edited=False,par_id=instance.id)
	else:
		Journal.objects.create(parent='item',created=False,edited=True,par_id=instance.id)
@receiver(post_save,sender=CommentItem)
def comment_added(sender,instance,created,**kwargs):
	if created:
		Journal.objects.create(parent='comment',created=True,edited=False,par_id=instance.id)
@receiver(post_save,sender=Files)
def file_added(sender,instance,created,**kwargs):
	if created:
		Journal.objects.create(parent='file',created=True,edited=False,par_id=instance.id)
@receiver(post_save,sender=TOBlank)
def tob_added(sender,instance,created,**kwargs):
	if created:
		Journal.objects.create(parent='tob',created=True,edited=False,par_id=instance.id)
	else:
		Journal.objects.create(parent='tob',created=False,edited=True,par_id=instance.id)
@receiver(post_save,sender=TOMonth)
def tom_added(sender,instance,created,**kwargs):
	if created:
		Journal.objects.create(parent='tom',created=True,edited=False,par_id=instance.id)
	else:
		Journal.objects.create(parent='tom',created=False,edited=True,par_id=instance.id)
@receiver(post_save,sender=Phone)
def phone_added(sender,instance,created,**kwargs):
	if created:
		Journal.objects.create(parent='phone',created=True,edited=False,par_id=instance.id)
	else:
		Journal.objects.create(parent='phone',created=False,edited=True,par_id=instance.id)
@receiver(post_save,sender=PhoneCat)
def phc_added(sender,instance,created,**kwargs):
	if created:
		Journal.objects.create(parent='phc',created=True,edited=False,par_id=instance.id)
	else:
		Journal.objects.create(parent='phc',created=False,edited=True,par_id=instance.id)
@receiver(post_save,sender=LocalObject)
def lobj_added(sender,instance,created,**kwargs):
	if created:
		Journal.objects.create(parent='lobj',created=True,edited=False,par_id=instance.id)
	else:
		Journal.objects.create(parent='lobj',created=False,edited=True,par_id=instance.id)
@receiver(post_save,sender=Task)
def lobj_added(sender,instance,created,**kwargs):
	if created:
		Journal.objects.create(parent='task',created=True,edited=False,par_id=instance.id)
	else:
		Journal.objects.create(parent='task',created=False,edited=True,par_id=instance.id)