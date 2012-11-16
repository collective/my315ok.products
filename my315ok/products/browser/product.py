#-*- coding: UTF-8 -*-
from five import grok
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from my315ok.products.product import Iproduct 

class view(grok.View):
    grok.context(Iproduct)
    grok.require('zope2.View')
    grok.name('view')

#    def update(self):
#        """
#        """
#        # Hide the editable-object border
##        context = self.context
##        request = self.request
#        self.request.set('disable_border', True)
##        catalog = getToolByName(self.context, 'portal_catalog')
        
#brain come from contained image field 's object
    def isImageAvalable(self,brain=None):
        """判断图片字段是否有效"""
        try:
            if brain is None:
                image = self.context.image.size
            else:
                 image = brain.getObject().image.size
                 
            return (image != 0)
#                return True
#            else:
#                return False
        except:
            return False
        
    def transfer2text(self,obj):
#        import pdb
#        pdb.set_trace()
        try:
            res = obj.output
            return res
        except:
            return obj
 
    def img_tag(self,scale=None,fieldname="image"):
        scales = getMultiAdapter((self.context, self.request), name='images')
        if scale == None:
            scale = scales.scale(fieldname, scale=scale)
        else:
            scale = scales.scale(fieldname, scale=scale)            
        imageTag = scale.tag()
        return imageTag


    def img_large_link(self,fieldname="image",large="large"):
        link = self.img_url() + "/" + fieldname + "_" + large
        return link
    def img_url(self):
        return self.context.absolute_url()        