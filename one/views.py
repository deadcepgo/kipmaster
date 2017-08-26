# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse
from models import Item,LocalObject,Tag,UploadFileForm,AddItem,Task,Files,CommentItem,Phone,PhoneCat,Journal,TOBlank,TOMonth,Treb

import re
import csv
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import xlrd
import time
import datetime
import calendar

from django.utils import timezone

def handle_uploaded_file(f):
    with open(f, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
def get_cats(thiscat,d):
	category_list = thiscat.get_descendants(include_self=True)
	locateitems = []
	for cat in category_list:
		if len(d.filter(lobject=cat))>0:
			cat_items = d.filter(lobject=cat)
			if len(cat_items)>0:
				for cat_item in cat_items:
					locateitems.append(cat_item)
	return locateitems
def proverka(next=False):
	to_bs = TOBlank.objects.all()
	
	for to_b in to_bs:
		if next == True:
			date_on = datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,to_b.dmn)
			date_deadline = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,to_b.dme)
		else:
			date_on = datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,to_b.dmn)
			date_deadline = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,to_b.dme)
		user = 'ROBOT'
		status = 'act'
		text = u'TO %s'%(to_b.name)
		if len(Task.objects.filter(date_on=date_on,user=user,text=text))==0:
			t = Task(date_on=date_on,date_deadline=date_deadline,user=user,status=status, text=text)
			t.save()
def make_pdf(request):
	if request.method == 'GET':
		tob = TOBlank.objects.get(id=int(request.GET.get('tobid')))
		month = request.GET.get('month')
		from mkpdf import *
		for lobject in tob.childs.all():
			osn_tab_dat = add_head_dat(osn_tab_dat,lobject.name)
			osn_tab_style = add_head_style(osn_tab_dat,osn_tab_style)
			count=1
			for item in lobject.items.all():
				if month is not None:
					month=int(month)
					osn_tab_dat = add_elem_dat(osn_tab_dat,[count,item.name,item.par_iz,'',item.mark,item.serial,item.date_pov,'ТО-%s'%lobject.get_to_num(mounth=month),'',''])
				else:
					osn_tab_dat = add_elem_dat(osn_tab_dat,[count,item.name,item.par_iz,'',item.mark,item.serial,item.date_pov,'ТО-%s'%lobject.get_to_num(),'',''])
				count+=1
		osn_tab = Table(osn_tab_dat,colWidths='*',repeatRows=1)
		osn_tab.setStyle(TableStyle(osn_tab_style))                 
		osn_tab._argW[0]=0.3*inch
		osn_tab._argW[1]=1.9*inch
		osn_tab._argW[2]=1.5*inch
		osn_tab._argW[3]=0.9*inch
		osn_tab._argW[4]=1.2*inch
		osn_tab._argW[5]=0.9*inch
		osn_tab._argW[6]=0.9*inch
		osn_tab._argW[7]=0.6*inch
		osn_tab._argW[8]=0.9*inch
		osn_tab._argW[9]=0.9*inch
		osn_tab._argH[0]=0.4*inch
		rowcount=0
		#osn_tab._argH[4]=0.18*inch
		#osn_tab._argH[3]=0.32*inch

		#for row in osn_tab._cellvalues:
		#	if rowcount == 0:
		#		rowcount+=1
		#		continue
		#	for col in row:				
		#		if col!='':
		#			print len(col.text)
		#		if col!='' and len(col.text)<80:
		#			
		#			osn_tab._argH[rowcount]=0.2*inch
		#		if col!='' and len(col.text)>=80:
		#			osn_tab._argH[rowcount]=0.3*inch
		#			break
		#	rowcount+=1
		#		elif col!='' and len(col.text)>100 and len(col.text)<120:
		#			osn_tab._argH[rowcount]=0.2*inch
		#		else:
		#			osn_tab._argH[rowcount]=0.2*inch
		#			break
			

		elements.append(osn_tab)
		
		
		footer_tab_dat = [
							[add_p('Работы выполнил:',bold=1),'','','',add_p('Выполнение работ подтверждаю:',bold=1),'',''],
							[add_p('Слесарь по КИПиА<br/>ООО "Снэма-Сервис"',bold=1,right='left'),add_p('_________________ /'),add_p('___________________________ /'),
							'',add_p('Представитель<br/>ТПП "ЛУКОЙЛ-Ухтанефтегаз"',bold=1,right='left'),add_p('_________________ /'),add_p('___________________________ /'),''],
							[add_p('ООО "Снэма-Сервис"',bold=1,size=6),add_p('(подпись)',size=5),add_p('(Фамилия И.О.)',size=5),'',
							add_p('ТПП "ЛУКОЙЛ-Ухтанефтегаз"',bold=1,size=6),add_p('(подпись)',size=5),add_p('(Фамилия И.О.)',size=5)],
							['',add_p('"____" ________________ 2017 г.',right='left'),'','','',add_p('"____" ________________ 2017 г.',right='left'),''],
							[''],
							[add_p('Мастер КИПиА<br/>ООО "Снэма-Сервис"',bold=1,right='left'),add_p('_________________ /'),add_p('___________________________ /'),],
							[add_p('ООО "Снэма-Сервис"',bold=1),add_p('(подпись)',size=5),add_p('(Фамилия И.О.)',size=5)],
							['',add_p('"____" ________________ 2017 г.',right='left')],
						]
		footer_style = [
						#('GRID',(0,0),(-1,-1),0.5,colors.black),
						('SPAN',(1,3),(2,3)),
						('SPAN',(1,7),(2,7)),
						('SPAN',(5,3),(6,3)),
						('SPAN',(0,0),(1,0)),
						('SPAN',(4,0),(5,0)),
						('SPAN',(0,1),(0,2)),
						('SPAN',(0,5),(0,6)),
						('SPAN',(4,1),(4,2)),
						#('VALIGN',(0,1),(-1,1),'BOTTOM'),
						#('VALIGN',(0,2),(-1,2),'BOTTOM'),
						]
              #('SPAN',(0,0),(-1,0)),
              #('SPAN',(0,1),(-1,1)),
              #('VALIGN',(0,0),(-1,-1),'MIDDLE'),]
		footer_tab = Table(footer_tab_dat,colWidths='*')
		footer_tab.setStyle(TableStyle(footer_style))
		footer_tab._argW[0]=1.5*inch
		footer_tab._argW[1]=1.15*inch
		footer_tab._argW[2]=1.7*inch
		footer_tab._argW[3]=1*inch
		footer_tab._argW[4]=1.6*inch
		footer_tab._argW[5]=1.15*inch
		footer_tab._argW[6]=1.7*inch
		footer_tab._argH[2]=0.15*inch
		footer_tab._argH[6]=0.15*inch
		elements.append(footer_tab)
		doc.build(elements)
		del doc
		del elements
		del footer_tab
		del footer_style
		del footer_tab_dat
		del osn_tab
		del osn_tab_dat
		del osn_tab_style
	return redirect('/')
def index(request):
	locations = LocalObject.objects.all()
	d = Item.objects.all()
	month = datetime.datetime.now().month
	year = datetime.datetime.now().year
	#in_this_month = d.filter(get_pov__contains=str(year))
	if request.GET.get('name')=='True':
		d = d.filter(name__icontains=request.GET.get('q').lower())
	if request.GET.get('serial')=='True':
		d = d.filter(serial__contains=request.GET.get('q'))
	if request.GET.get('date_p')=='True':
		d = d.filter(date_pov=request.GET.get('q'))
	if request.GET.get('mark')=='True':
		d = d.filter(mark__icontains=request.GET.get('q'))
	if request.GET.get('model')=='True':
		d = d.filter(model__icontains=request.GET.get('q'))
	if request.GET.get('locate'):
		parent 		= LocalObject.objects.get(id=int(request.GET.get('locate')))
		thiscat 	= LocalObject.objects.get(id=parent.id)
		d = get_cats(thiscat,d)
	if request.GET.get('dattype')=='True':
		d = d.filter(dattype__icontains=request.GET.get('q'))
	paginator 		= Paginator(d,20)
	
	page = request.GET.get('page')
	try:
		d = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		d = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		d = paginator.page(paginator.num_pages)
		

	return render(request,'templates/index.html', locals())

def item(request):
	if request.GET.get('d_id'):
		
		d 				= Item.objects.get(id=int(request.GET.get('d_id')))
		if request.POST.get('text'):
			user = request.POST.get('user')
			text = request.POST.get('text')
			c = CommentItem(user=user,text=text,par='item',par_id=str(d.id))
			c.save()
		files 			= Files.objects.all().filter(parent='item', parent_id=d.id)
		comments		= CommentItem.objects.filter(par='item',par_id=str(d.id)).order_by('-date_pub')


		#request.POST.get('file')
		#request.POST.get('')
		#request.POST.get('')

	return render(request,'templates/item.html',locals())
def item_change(request):
	
	tags 				= Tag.objects.all()
	lobjs 				= LocalObject.objects.all()
	
	if request.GET.get('d_id'):
		d = Item.objects.get(id=int(request.GET.get('d_id')))
		files 			= Files.objects.all().filter(parent='item', parent_id=d.id)
		form 			= UploadFileForm(instance=d)
		form.fields['name'].label = "Имя файла"
		form.fields['document'].label = "Файл"
		if request.GET.get('delfile'):
			file_id = int(request.GET.get('del_id'))
			parent_id = int(request.GET.get('par_id'))
			file_to_del = Files.objects.get(id=file_id)
			#file_to_del = [file_id,parent_id]
			file_to_del.parent_id.remove(d)
			file_to_del.save()
		if request.POST.get('name') or request.POST.get('pe') or request.POST.get('bir_tr') or request.POST.get('bir_pr') or request.POST.get('mark') or request.POST.get('model') or request.POST.get('serial') or request.POST.get('date_pov') or request.POST.get('date_cal'): 
			d.name 		= request.POST.get('name')
			d.mark 		= request.POST.get('mark')
			d.model 	= request.POST.get('model')
			d.serial 	= request.POST.get('serial')
			d.date_pov 	= request.POST.get('date_pov')
			d.date_cal 	= request.POST.get('date_cal')
			d.date_mk 	= request.POST.get('date_mk')
			d.par 		= request.POST.get('par')
			d.active 	= request.POST.get('active')
			d.dattype 	= request.POST.get('dattype')
			d.lobject.clear()
			d.lobject.add(LocalObject.objects.get(id=int(request.POST.get('lobject'))))
			d.ti 		= request.POST.get('ti')
			d.greer 	= request.POST.get('greer')
			d.min_z 	= request.POST.get('min_z')
			d.max_z 	= request.POST.get('max_z')
			d.sig 		= request.POST.get('sig')
			d.mpi 		= request.POST.get('mpi')
			d.sr_sl 	= request.POST.get('sr_sl')
			d.par_iz 	= request.POST.get('par_iz')
			d.otm_o_pov = request.POST.get('otm_o_pov')
			d.pe 		= request.POST.get('pe')
			d.bir_tr 	= request.POST.get('bir_tr')
			d.bir_pr 	= request.POST.get('bir_pr')
			if request.POST.get('tags'):
				tagi = request.POST['tags']
				if len(request.POST.getlist('tags'))>0:
					d.tags.clear()
					for tag_id in request.POST.getlist('tags'):
						d.tags.add(Tag.objects.get(id=tag_id))
			else:
				d.tags.clear()

			d.save()
			
			return redirect('/item/?d_id='+str(d.id))
	else:
		d = False
	
	return render(request,'templates/itemchange.html',locals())
def item_add(request):
	tags 				= Tag.objects.all()
	lobjs 				= LocalObject.objects.all()
	if request.method == 'POST':
		name 			= request.POST.get('name')
		mark 			= request.POST.get('mark')
		model 			= request.POST.get('model')
		serial 			= request.POST.get('serial')
		date_pov 		= request.POST.get('date_pov')
		date_cal 		= request.POST.get('date_cal')
		date_mk 		= request.POST.get('date_mk')
		par 			= request.POST.get('par')
		active 			= request.POST.get('active')
		dattype 		= request.POST.get('dattype')
		locate 			= LocalObject.objects.get(id=request.POST.get('lobject'))
		ti 				= request.POST.get('ti')
		greer 				= request.POST.get('greer')
		min_z 				= request.POST.get('min_z')
		max_z 				= request.POST.get('max_z')
		sig 				= request.POST.get('sig')
		mpi 				= request.POST.get('mpi')
		sr_sl 				= request.POST.get('sr_sl')
		par_iz 				= request.POST.get('par_iz')
		otm_o_pov 				= request.POST.get('otm_o_pov')

		d 				= Item(name=name,mark=mark,model=model,serial=serial,date_pov=date_pov,date_cal=date_cal,date_mk=date_mk,par=par,active=active,dattype=dattype,ti=ti,greer=greer,min_z=min_z,max_z=max_z,sig=sig,mpi=mpi,sr_sl=sr_sl,otm_o_pov=otm_o_pov,par_iz=par_iz)
		d.save()
		d.lobject.add(locate)
		d.save()
		return redirect('/')
	else:
		try:
			lobj_id = int(request.GET.get('lobj'))
		except:
			pass
	return render(request,'templates/itemadd.html',locals())

def locations(request):
	nodes = LocalObject.objects.all()
	return render(request,'templates/locations.html',locals())
def imp_b(request):
	import xlrd
	###БАЗА ЛУКОЙЛ ПО ДАТЧИКАМ ИМПОРТ###
	rb = xlrd.open_workbook('/home/serega/to/obisikcdng2.xls',formatting_info=True)
	
	sheet = rb.sheet_by_index(0)
	activ = False
	for val in xrange(7,1115):
		if len(sheet.row_values(val)[1])>0 and activ is False:
			lobj 		= sheet.row_values(val)[1]
			
			activ 		= True
		elif len(sheet.row_values(val)[1])>0 and activ is True:
			#пакуем данные по прибору
			lobj 		= sheet.row_values(val)[1]
		
		else:
			pass
		if activ is True:
			item 		= Item()
			item.name 	= sheet.row_values(val)[2][0:1].upper()+sheet.row_values(val)[2][1:]
			if item.name==' ':
				item.name='######'
			item.ti 	= sheet.row_values(val)[3]
			item.mark 	= sheet.row_values(val)[4]
			item.model 	= sheet.row_values(val)[5]
			item.greer 	= sheet.row_values(val)[6]
			item.min_z 	=  sheet.row_values(val)[7]
			item.max_z 	= sheet.row_values(val)[8]
			item.sig 	= sheet.row_values(val)[9]
			item.mpi 	= sheet.row_values(val)[10]
			item.par 	= sheet.row_values(val)[11]
			item.date_mk =  sheet.row_values(val)[12]
			item.sr_sl 	= sheet.row_values(val)[13]
			item.serial = sheet.row_values(val)[14]
			item.par_iz = sheet.row_values(val)[15]
			item.status = sheet.row_values(val)[16]
			item.otm_o_pov = sheet.row_values(val)[17]
        	item.dattype = lobj
        	item.save()
	return redirect('/')
def imp_b2(request):
	xls = '/home/serega/oborud.xls'
	rb = xlrd.open_workbook(xls,formatting_info=True)
	sheet = rb.sheet_by_index(0)
	for x in xrange(0,802):

		name = sheet.row_values(x)[0]
		par_iz = sheet.row_values(x)[1]
		mm = sheet.row_values(x)[3]
		serial = sheet.row_values(x)[4]
		dpp = sheet.row_values(x)[5]
		obj = sheet.row_values(x)[6]
		nadobj = sheet.row_values(x)[7]
		location = sheet.row_values(x)[8]
		Item.objects.create(name=name,model=mm,par_iz=par_iz,serial=serial,date_pov=dpp,dattype=obj+' '+nadobj+' '+location)
		print x,name,par_iz,mm,serial,dpp,obj,nadobj,location
	
	return redirect('/')

def uploadfile(request):
	if request.method == 'POST':
		# Заполняем форму полученными данными
		
		form 			= UploadFileForm(request.POST, request.FILES)
		ref 			= request.META['HTTP_REFERER']
		did 			= int(re.findall(r'\d+',ref)[-1:][0])
		# Если данные валидны
		if form.is_valid():
			# обрабатываем файл
			
			form.save()
		
		#	# перенаправляем на другую страницу
		return redirect('/item/?d_id='+str(did))
	return redirect('/')
def save_to(request):
	items = Item.objects.all()
	with open('lobjects_csv') as csv_file:
		csv_writer = csv.writer(csv_file)
def read_from(request):
	with open('/var/www/chpkip/new/lobjects_csv1','rb') as csv_file:
		csv_reader = csv.reader(csv_file)
		los={}
		for row in csv_reader:
			l = LocalObject(name = row[1],to_yan=row[3],to_main=row[4])
			l.save()
			los[row[0]]=l
			if len(row[2])>0:
				try:
					l.parent = LocalObject.objects.get(id=los[row[2]].id)
					l.save()
				except:
					pass

	return redirect('/')
def savec_csv(request):
	with open('/var/www/chpkip/new/lobjects_csv1','wb') as csv_file:
		csv_writer = csv.writer(csv_file)
		lobjs = LocalObject.objects.all()
		for lobj in lobjs:
			
			if type(lobj.parent)!=type(None):
				csv_writer.writerow([lobj.id,lobj.name.encode('utf-8'),lobj.parent.id,lobj.to_yan,lobj.to_main])
			else:
				csv_writer.writerow([lobj.id,lobj.name.encode('utf-8'),'',lobj.to_yan,lobj.to_main])
	return redirect('/')
def phonecats(request):
	nodes = PhoneCat.objects.all()
	return render(request,'templates/phonecats.html',locals())
def phones(request):
	if request.GET.get('cat'):
		cat = int(request.GET.get('cat'))
		phones = Phone.objects.all()		
		if len(str(cat))>0:
			parent 			= PhoneCat.objects.get(id=cat)
			thiscat 		= PhoneCat.objects.get(id=parent.id)
			category_list 	= thiscat.get_descendants(include_self=True)
			
			for cat in category_list:
				if len(phones.filter(cat=cat))>0:
					phones 	=	phones.filter(cat=cat)
	else:
		phones = Phone.objects.all()
	
		
	return render(request,'templates/phones.html',locals())
def journal(request):
	journal = Journal.objects.all().order_by('-time')
	paginator 		= Paginator(journal,20)
	
	page = request.GET.get('page')
	try:
		journal = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		journal = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		journal = paginator.page(paginator.num_pages)
	return render(request,'templates/journal.html',locals())


def to(request):
	if request.GET.get('par'):
		tob = TOBlank.objects.get(id=int(request.GET.get('par')))
		childs = tob.childs.all()#LocalObject.objects.filter(parent=parent)
		#pods = []
		if request.GET.get('mounth'):
			mounth = int(request.GET.get('mounth'))
		else:
			mounth = 1
		
	if request.GET.get('print'):
		if request.GET.get('print')=='True':
			#make_pdf(request)
			pass
	return render(request,'templates/test.html',locals())

def kcdngto(request):
	golova = request.GET.get('golova')
	gol_dol = request.GET.get('gol_dol')
	gol_pl = request.GET.get('gol_pl')
	gol_dpl = request.GET.get('gol_dpl')
	asup = request.GET.get('asup')
	kip_mas = request.GET.get('kip_mas')
	month = request.GET.get('month')
	year = request.GET.get('year')
	prev_month = request.GET.get('prev_month')
	main_objs = []
	for tobj in TOMonth.objects.all():
		if len(tobj.childs.all())<1:
			main_objs.append(tobj)
	return render(request,'templates/kcdngto.html',locals())
def toobj(request):
	if request.POST.get('to'):
		redirect(u'/to/kcdng/')
		to = request.POST.get('to')
		if to == '1':#KCDNG
			if request.POST.get('kcdng_rul') == '1':
				golova = u'Болсун С.А.'
				gol_dol = u'Начальник'
				gol_pl = u'Болсуна С.А.'
				gol_dpl = u'Начальника'
			elif request.POST.get('kcdng_rul') == '2':
				golova = u'Тодесеев С.В.'
				gol_dol = u'Заместитель начальника'
				gol_pl = u'Тодесеева С.В.'
				gol_dpl = u'Заместителя начальника'
			asup = request.POST.get('kcdng_asup')
			kip_mas = request.POST.get('kip_mas')
			month = request.POST.get('month')
			year = request.POST.get('year')
			
			if month == '01':
				prev_month = '12'
			else:
				prev_month = int(month)-1
				if len(str(prev_month))<2:
					prev_month = '0'+str(prev_month)
				else:
					prev_month = str(prev_month)

			return redirect(u'/to/kcdng/?golova='+golova+'&gol_dol='+gol_dol+'&asup='+asup+'&kip_mas='+kip_mas+'&month='+month+'&year='+year+'&prev_month='+prev_month+'&gol_dpl='+gol_dpl+'&gol_pl='+gol_pl)
	else:
		main_objs	= TOBlank.objects.all()
	return render(request,'templates/toobjs.html',locals())
def lobjpage(request):
	if request.method == 'GET':
		parent_id = request.GET.get('locate')
		
		try:
			files = Files.objects.filter(parent='lobj',parent_id=int(parent_id))
		except:
			files=[]
		parent = LocalObject.objects.get(id=int(parent_id))
		subitems = get_cats(parent,Item.objects.all())
		if len(subitems)>15:
			paginator 		= Paginator(subitems,20)
			page = request.GET.get('page')
			try:
				subitems = paginator.page(page)
			except PageNotAnInteger:
				subitems = paginator.page(1)
			except EmptyPage:
				subitems = paginator.page(paginator.num_pages)
		comments = CommentItem.objects.filter(par='lobject',par_id=parent_id).order_by('-date_pub')
	elif request.method == 'POST':
		par_id = request.GET.get('par_id')
		user = request.POST.get('user')
		text = request.POST.get('text')
		CommentItem.objects.create(user=user,text=text,par='lobject',par_id=str(par_id))
		return redirect('/lobject/?par_id='+par_id)
	#files = 
	return render(request,'templates/lobj.html',locals())
def tasks(request):
	proverka()
	today = datetime.date.today()
	if request.method == 'GET':
		day = request.GET.get('day')
		if day == 'today':
			tasks = Task.objects.exclude(status='end').order_by('date_on')
		elif day == 'tomorow':
			tasks = Task.objects.filter(date_on=today+datetime.timedelta(days=1))
		elif day == 'week':
			today = datetime.date.today()
			monday = today - datetime.timedelta(datetime.datetime.weekday(today))
			sunday = today + datetime.timedelta(6 - datetime.datetime.weekday(today))
			tasks = Task.objects.filter(date_on__range=[monday,sunday])
		elif day == 'month':
			today = datetime.date.today()
			month_start = today - datetime.timedelta(days=int(today.day)-1)
			month_end = month_start + datetime.timedelta(days=calendar.mdays[today.month]-1)
			tasks = Task.objects.filter(date_on__range=[month_start,month_end])
		elif day == 'year':
			today = datetime.date.today()
			tasks = Task.objects.filter(date_on__range=[datetime.date(today.year,1,1),datetime.date(today.year,12,31)])
		elif day == 'interval':
			int_start = request.GET.get('int_start')
			int_end = request.GET.get('int_end')
			tasks = Task.objects.filter(date_on__range=[int_start,int_end])
		else:
			tasks = Task.objects.all()
	return render(request,'templates/tasks.html',locals())
def task(request):
	lobjects = LocalObject.objects.all()
	if request.method == 'GET':
		task = Task.objects.get(id=int(request.GET.get('tid')))
		files = Files.objects.filter(parent='task',parent_id=int(request.GET.get('tid')))
		comments = CommentItem.objects.filter(par='task',par_id=request.GET.get('tid'))
		if request.GET.get('change')=='True':
			return render(request,'templates/taskchange.html',locals())
		else:
			return render(request,'templates/task.html',locals())
	elif request.method == 'POST':
		par_id = request.GET.get('tid')
		if request.POST.get('is_comment')=='True':
			user = request.POST.get('user')
			text = request.POST.get('text')
			CommentItem.objects.create(user=user,text=text,par='task',par_id=str(par_id))
		else:
			t 				= Task.objects.get(id=int(par_id))
			t.date_on 		= request.POST.get('date_on')
			predline = request.POST.get('date_dline').split('-')
			t.date_deadline 	= datetime.datetime(int(predline[0]),int(predline[1]),int(predline[2]),tzinfo=timezone.utc)#int(predline[0]),int(predline[1]),int(predline[2]))
			t.text 			= request.POST.get('text')
			t.status 			= request.POST.get('status')
			if len(request.POST.get('lobj'))>0:
				t.lobj 			= LocalObject.objects.get(id=int(request.POST.get('lobj')))
			t.save()
			
		return redirect('/task/?tid='+par_id)

def addtask(request):
	lobjects = LocalObject.objects.all()
	if request.method == 'POST':
		user = request.POST.get('user')
		text = request.POST.get('text')
		date_on = request.POST.get('date_on')
		date_deadline = request.POST.get('date_deadline')
		t = Task(user=user,text=text,date_on=date_on)

		if len(date_deadline)>0:
			t.date_deadline = date_deadline
		if len(request.POST.get('lobj'))>0:
			t.lobj = LocalObject.objects.get(id=int(request.POST.get('lobj')))
		t.save()
		return redirect('/tasks/?day=today')
	return render(request,'templates/addtask.html',locals())
def needs(request):
	
	if request.method == 'POST':
		name = request.POST.get('name')
		num = int(request.POST.get('col'))
		t = Treb(name=name,col=num)
		lobj = LocalObject.objects.get(id=int(request.POST.get('obj')))
		t.save()
		try:
			
			t.obj.add(lobj)
		except:
			pass
		t.save()
		
	need = Treb.objects.all()
	lobjs = LocalObject.objects.all()
	
	return render(request,'templates/needs.html',locals())
def kusty(request):
	plcs_m = Plc.objects.using('CDNG2').filter(id_base_station=3)
	plcs_s = Plc.objects.using('CDNG2').filter(id_base_station=2)
	plcs_b = Plc.objects.using('CDNG2').filter(id_base_station=4)
	plcs_v = Plc.objects.using('CDNG2').filter(id_base_station=1)
	n = Ninja.objects.all()
	if request.method == "POST":
		plc_id = int(request.POST.get('plc_id'))
		status = request.POST.get('status')
		if status == 'True':
			status = u'Норм'
		else:
			status = u'Не включать!'
		plc_n = Ninja.objects.get(plc_id=plc_id)
		plc_n.status = status
		plc_n.save()
	return render(request,'templates/kusty.html',locals())
def docs(request):
	documents = Files.objects.all().order_by('-date_pub')
	return render(request,'templates/docs.html',locals())