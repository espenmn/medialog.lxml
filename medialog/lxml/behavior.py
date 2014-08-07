from zope import schema
#from plone.directives import dexterity
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('medialog.lxml')
 
class IScrape(form.Schema):
    """ Settings for scrape_view"""
    scrape_url = schema.URI(
        title = _("label_scrape_url", default=u"URL"),
        description = _("help_scrape_url",
        default="Path to content to embedd"),
        default='http://somesite.com/some/path',
    )

    scrape_selector = schema.ASCIILine(
        title = _("label_scrape_selector", default=u"Selector"),
         description = _("help_scrape_selector",
        default="An id or class to filter content on"),
           default='#content',
    )

alsoProvides(IScrape, IFormFieldProvider)

