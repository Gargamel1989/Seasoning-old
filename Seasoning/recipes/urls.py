"""
Copyright 2012, 2013 Driesen Joep

This file is part of Seasoning.

Seasoning is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Seasoning is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Seasoning.  If not, see <http://www.gnu.org/licenses/>.
    
"""
from django.conf.urls import patterns, url
from recipes.views import delete_recipe_comment

urlpatterns = patterns('',
    url(r'^$', 'recipes.views.browse_recipes', name='recipe_browse'),
    url(r'^search/$', 'recipes.views.search_recipes', name='recipe_search'),
    url(r'^(\d*)/$', 'recipes.views.view_recipe', name='recipe_view'),
    url(r'^(\d*)/portions/(\d*)/$', 'recipes.views.view_recipe'),
    url(r'^vote/(\d*)/(\d*)/$', 'recipes.views.vote'),
    url(r'^removevote/(\d*)/$', 'recipes.views.remove_vote'),
    url(r'^deletecomment/(\d)/(\d)/$', delete_recipe_comment),
    
    url(r'^add/$', 'recipes.views.edit_recipe'),
    url(r'^edit/(\d*)/$', 'recipes.views.edit_recipe'),
    
    url(r'mine/$', 'recipes.views.my_recipes'),
)
