from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^item/$', views.item, name='item'),
    url(r'^item/change/$', views.item_change, name='itemchange'),
    url(r'^item/add/$', views.item_add, name='itemadd'),
    url(r'^locations/$', views.locations, name='locations'),
    url(r'^phonecats/$', views.phonecats, name='phonecats'),
    url(r'^phones/$', views.phones, name='phones'),
    url(r'^uploadfile/$', views.uploadfile, name='uploadfile'),
    url(r'^save_to/$', views.imp_b2, name='save_to'),
    url(r'^sl_to/$', views.savec_csv, name='save_to'),
    url(r'^read_from/$', views.read_from, name='read_from'),
    url(r'^to/$', views.to, name='to'),
    url(r'^to/kcdng/$', views.kcdngto, name='kcdngto'),
    url(r'^toobjs/$', views.toobj, name='toobjs'),
    url(r'^journal/$', views.journal, name='journal'),
    url(r'^make_pdf/$', views.make_pdf, name='make_pdf'),
    url(r'^lobject/$', views.lobjpage, name='lobject'),
    url(r'^tasks/$', views.tasks, name='tasks'),
    url(r'^task/$', views.task, name='task'),
    url(r'^addtask/$', views.addtask, name='task'),
    url(r'^needs/$', views.needs, name='needs'),
    url(r'^kusty/$', views.kusty, name='kusty'),
    url(r'^docs/$', views.docs, name='docs'),
]
