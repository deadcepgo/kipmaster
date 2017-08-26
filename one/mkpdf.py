# -*- coding: utf-8 -*-
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape,letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.pdfbase import ttfonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

styleSheet=getSampleStyleSheet()

font = r'C:\\seregatm\\123\\ofont.ru_ArialCyr.ttf'
font2 = r'C:\\seregatm\\123\\ofont.ru_ArialCyrB.ttf'
pdfmetrics.registerFont(TTFont("ArialCyr", font))
pdfmetrics.registerFont(TTFont("ArialCyrB", font2))
doc = SimpleDocTemplate("C:\\seregatm\\123\\simple_table.pdf", pagesize=landscape(letter), topMargin=0.2*inch,bottomMargin=0.2*inch)
# container for the 'Flowable' objects
elements = []

osn_tab_style = [('GRID',(0,0),(-1,-1),0.5,colors.black),
         ('ALIGN',(0,0),(-1,-1),'CENTER'),
         ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
         #('LEADING',(0,0),(-1,0),1000),
         ('TOPPADDING',(0,0),(-1,-1),2),
         ('BOTTOMPADDING',(0,0),(-1,-1),0),
         ('FONTSIZE',(0,0),(-1,-1),7),
         ('FONTNAME',(0,0),(-1,-1),"ArialCyr")]
def add_p(text,right=None,bold=None,size=None):
    #return Paragraph('''<para align=center spaceb=3><font name='ArialCyr' size=7><b>%s</b></font></para>'''%text,styleSheet["Normal"])
    p = '''<para align=%s spaceb=3><font name='%s' size=%s>%s</font></para>'''
    if size is not None:
      fsize = size
    else:
      fsize = 7
    if bold is not None:
      fontn = 'ArialCyrB'
    else:
      fontn = 'ArialCyr'
    if right is not None:
      pos = 'right'
    if right=='center':
      pos = 'center'
    elif right=='left':
      pos = 'left'
    elif right=='right':
      pos = 'right'
    
    else:
      pos = 'center'
    p = p%(pos,fontn,fsize,text)
    return Paragraph(p,styleSheet["BodyText"])
    
def add_head_dat(data,text):
    data.append([add_p(text),'','','','','','','','',''])
    return data
def add_head_style(data,style):
    row = len(data)-1
    style.append(('SPAN',(0,row),(-1,row)))
    return style
def add_elem_dat(data,parametres):
    data.append([add_p(parametres[0],size=7),add_p(parametres[1],size=6),add_p(parametres[2],size=6),add_p(parametres[3],size=6),add_p(parametres[4],size=6),add_p(parametres[5],size=6),
                add_p(parametres[6],size=6),add_p(parametres[7],size=6),add_p(parametres[8],size=6),add_p(parametres[9],size=6)])
    return data
data = [[add_p('Акт',size=10), '', '', '', ''],
       [add_p('проведения планово-предупредительных работ средств автоматизации КЦДНГ-2 ТПП "ЛУКОЙЛ-Ухтанефтегаз"',size=10), '', '', '', ''],
       ['', '', '', '', ''],
       [ add_p('Объект:',right='right',bold=1),'', '', add_p('%Название объекта%',bold=1), ''],
       [add_p('Код объекта:',right='right',bold=1),'', '' , '', ''],
       [add_p('Дата проведения:',right='right',bold=1),'', '' , add_p('с   "_____"_____________________2017г'), ''],
       ['', '', '', add_p('по "_____"_____________________2017г'), ''],
       ['', '', '', '', ''],
       ]
base_style = [
              ('SPAN',(0,0),(-1,0)),
              ('SPAN',(0,1),(-1,1)),
              ('SPAN',(0,3),(1,3)),
              ('SPAN',(0,4),(1,4)),
              ('SPAN',(0,5),(1,5)),
              ('VALIGN',(0,0),(-1,-1),'MIDDLE'),]
head_tab = Table(data,colWidths='*')
head_tab.setStyle(TableStyle(base_style))
head_tab._argW[0]=0.3*inch
head_tab._argW[1]=1*inch
head_tab._argW[2]=0.3*inch
head_tab._argW[3]=2.1*inch
head_tab._argW[4]=6.3*inch
elements.append(head_tab)
osn_tab_dat = [
                  [add_p('№ п/п'), add_p('Наименование'), add_p('Контролируемый параметр, место установки'),add_p('Позиция'), add_p('Марка, тип'),
                   add_p('Серийный номер'),add_p('Дата последней поверки'), add_p('Вид ТО'), add_p('Состояние оборудования'),add_p('Примечание')],
              ]
#osn_tab_dat = add_head_dat(osn_tab_dat,'Насосный агрегат №1')
#osn_tab_style = add_head_style(osn_tab_dat,osn_tab_style)
#osn_tab_dat = add_elem_dat(osn_tab_dat,['','Ультразвукововй уровнемер L=12000мм','Уровень в РВС-1','','ДУУ 2М','20219','11.2016',
#                                        'ТО-1','',''])






