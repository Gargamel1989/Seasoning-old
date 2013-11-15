from django.test import TestCase
from django_dynamic_fixture import G
from authentication.models import User
from recipes.models import Cuisine

class RecipeViewsTestCase(TestCase):
    
    def setUp(self):
        self.user = G(User, is_active=True)
        self.user.set_password('test')
        self.user.save()
        G(Cuisine, name='Andere')
    
#    def test_view_recipe(self):
#        resp = self.client.get('/recipes/1/')
#        self.assertEqual(resp.status_code, 200)
#        
#        self.assertNumQueries(4, lambda: self.client.get('/recipes/1/'))
    
    def test_edit_recipe(self):
        location = '/recipes/add/'
        resp = self.client.get(location)
        # Need to be logged in first
        self.assertRedirects(resp, '/login/?next=' + location, 302, 200)
        
        self.client.post('/login/', {'username': self.user.email,
                                     'password': 'test'})
        resp = self.client.get(location)
        
        self.assertTrue('recipe_form' in resp.context)
        self.assertTrue(resp.context['new_recipe'])
        