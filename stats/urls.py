from django.conf.urls import patterns, include, url
from django.contrib import admin
from stats.views import StatsView
from django.contrib.auth.decorators import login_required, permission_required

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # sample stats pages
    
    url(r'^$', StatsView.as_view(template_name='statistics/p_report.html')),
    url(r'^custom.html$', StatsView.as_view(template_name='statistics/sgvizler.html')),
    url(r'^age.html$', StatsView.as_view(template_name='statistics/age.htm')),
    url(r'^birthplaces.html$', StatsView.as_view(template_name='statistics/birthplaces.htm')),
    url(r'^culture.html$', StatsView.as_view(template_name='statistics/culture.htm')),
    url(r'^gender.html$', StatsView.as_view(template_name='statistics/gender.htm')),
    url(r'^help.html$', StatsView.as_view(template_name='statistics/help_page.htm')),
    url(r'^language.html$', StatsView.as_view(template_name='statistics/language.htm')),
    url(r'^professional_category.html$', StatsView.as_view(template_name='statistics/professional_category.htm')),
    url(r'^query.html$', StatsView.as_view(template_name='statistics/query.htm')),
    url(r'^stats.html$', StatsView.as_view(template_name='statistics/stats.htm')),
    #url(r'^$', login_required(StatsView.as_view(template_name='statistics/p_report.html'))),

    #url(r'^$', StatsView.as_view(template_name='statistics/p_report.html')), 
    

    
    
   )
