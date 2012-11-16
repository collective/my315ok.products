import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import logout

from my315ok.products.testing import MY315OK_PRODUCTS_INTEGRATION_TESTING

from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from Products.CMFCore.utils import getToolByName

from my315ok.products.portlets import hot_goods_portlet as myportlet

class TestPortlet(unittest.TestCase):

    layer = MY315OK_PRODUCTS_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.products.productfolder', 'productfolder1')
        
        portal['productfolder1'].invokeFactory('my315ok.products.product','product1')
        portal['productfolder1'].invokeFactory('my315ok.products.product','product2')
        portal['productfolder1'].invokeFactory('my315ok.products.product','product3') 
        self.portal = portal                


    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='my315ok.products.portlets.hot_goods_portlet')
        self.assertEquals(portlet.addview, 'my315ok.products.portlets.hot_goods_portlet')

    def testInterfaces(self):
        portlet = myportlet.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portal = self.layer['portal']
        
        portlet = getUtility(IPortletType, name='my315ok.products.portlets.hot_goods_portlet')
        mapping = portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], myportlet.Assignment))

    def testRenderer(self):
        context = self.layer['portal']
        request = self.layer['request']
        
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=context)
        assignment = myportlet.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, myportlet.Renderer))

class TestRenderer(unittest.TestCase):
    
    layer = MY315OK_PRODUCTS_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.products.productfolder', 'productfolder1')
        
        portal['productfolder1'].invokeFactory('my315ok.products.product','product1')
        portal['productfolder1'].invokeFactory('my315ok.products.product','product2')
        portal['productfolder1'].invokeFactory('my315ok.products.product','product3')        
        self.membership = getToolByName(portal, 'portal_membership')

        self.portal = portal
                    

    
    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        portal = self.layer['portal']
        
        context = context or portal
        request = request or self.layer['request']
        
        view = view or portal.restrictedTraverse('@@plone')
        
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=portal)
        assignment = assignment or myportlet.Assignment()

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

