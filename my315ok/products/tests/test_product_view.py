#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from my315ok.products.testing import MY315OK_PRODUCTS_FUNCTIONAL_TESTING 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest

class TestProductlView(unittest.TestCase):
    
    layer = MY315OK_PRODUCTS_FUNCTIONAL_TESTING
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.products.productfolder', 'productfolder1')
        
        portal['productfolder1'].invokeFactory('my315ok.products.product','product1',title="product1")
        portal['productfolder1'].invokeFactory('my315ok.products.product','product2')
        portal['productfolder1'].invokeFactory('my315ok.products.product','product3')        


        self.portal = portal
        
    def test_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        
        page = portal.absolute_url() + '/productfolder1/product1/@@view'
        browser.open(page)
        open('/tmp/test.html', 'w').write(browser.contents)

        self.assertTrue('<h1 class="documentFirstHeading">product1</h1>' in browser.contents)
        
