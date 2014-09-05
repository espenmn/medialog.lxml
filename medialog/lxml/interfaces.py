from zope import schema
from zope.interface import Interface
from z3c.form import interfaces
from zope.interface import alsoProvides
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider

from collective.z3cform.datagridfield import DataGridFieldFactory 
from collective.z3cform.datagridfield.registry import DictRow

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('medialog.lxml')


class ILxmlLayer(Interface):
    """A layer specific to medialog.lxml
        """

#url class/id pair
class IUrlPair(form.Schema):
    scrape_base_url = schema.URI(
        title=_(u'scrape_base_url', 'URL to corresponding selector'), 
        required=False
    )
    scrape_selector = schema.ASCIILine(
        title=_(u'scrape_selector', 'CSS selector to filter on'),
        required=False
    )

#tags
class IScrapeTags(form.Schema):
    scrape_tags = schema.ASCIILine(
        title=_(u'scrape_tags', 'CSS tags'),
        required=False,
    )

    scrape_tags_description = schema.ASCIILine(
        title=_(u'scrape_tags_description', 
            'Description (optional, just to remember why you put it there'),
        required=False,
    )

class ILxmlSettings(form.Schema):
    """Adds settings to medialog.controlpanel
        """
    form.fieldset(
        'lxml',
        label=_(u'lmxl embedding'),
            fields=[
                    'scrape_url',
                    'scrape_url_pair',
                    'scrape_host_whitelist',
                    'scrape_javascript',
                    'scrape_scripts',
                    'scrape_comments',
                    'scrape_style',
                    'scrape_links',
                    'scrape_meta',
                    'scrape_page_structure',
                    'scrape_processing_instructions',
                    'scrape_embedded',
                    'scrape_frames',
                    'scrape_forms',
                    'scrape_annoying_tags',
                    'scrape_remove_tags',
                    'scrape_allow_tags',
                    'scrape_kill_tags',
                    'scrape_remove_unknown_tags',
                    'scrape_safe_attrs_only',
                    'scrape_add_nofollow',
                    'scrape_whitelist_tags',
            ],
    )
    
    form.widget(scrape_url_pair=DataGridFieldFactory)
    scrape_url_pair = schema.List(
        title = _(u"scrape_url_pair", 
            default=u"URL selector pairs"),
        value_type=DictRow(schema=IUrlPair),
    )
                  
    scrape_url = schema.URI(
        title=_(u"scrape_url", 
            default=u"Default URL"),
    )
                      
    scrape_safe_attrs_only = schema.Bool(
        title=_(u"scrape_safe_attrs_only", default=u"Security:Only permit safe attr"),
        description=_(u"help_safe_attrs_only",
            default="""If true, only include 'safe' attributes (specifically the list
                from http://feedparser.org/docs/html-sanitization.html""")
    )
    
    scrape_javascript = schema.Bool(
        title=_(u"scrape_javascript", 
            default=u"Security: Filter out javascript"),
        description=_(u"help_scrape_javascript",
            default="Removes any Javascript, like an ``onclick`` attribute.")
    )

    scrape_style = schema.Bool(
        title=_(u"scrape_style", 
            default=u"Security: Filter out CSS styles"),
        description=_(u"help_scrape_style",
            default="Removes any style tags or attributes.")
    )
    

    scrape_scripts  = schema.Bool(
        title=_(u"scrape_scripts", 
            default=u"Security: Remove scripts"),
        description=_(u"help_scrape_scripts",
            default="Removes any 'script' tags.")
    )

    scrape_comments  = schema.Bool(
        title=_(u"scrape_comments", 
            default=u"Removes comments"),
        description=_(u"help_scrape_comments",
            default="Removes any comments.")
    )
 
    scrape_links = schema.Bool(
        title=_(u"scrape_links", 
            default=u"Security: R'emove links"),
        description=_(u"help_scrape_links",
            default=" Removes any `link` tags")
    )


    scrape_meta = schema.Bool(
        title=_(u"scrape_meta", 
            default=u"Remove Meta tags"),
        description=_(u"help_scrape_meta",
            default="Removes any `meta` tags")
    )
    
    scrape_page_structure = schema.Bool(
        title=_(u"scrape_page_structure", 
            default=u"Structural parts"),
        description=_(u"help_scrape_page_structure",
            default="Structural parts of a page: 'head', 'html', 'title'.")
    )
 
    scrape_processing_instructions = schema.Bool(
        title=_(u"scrape_processing_instructions", 
            default=u"Processing instructions"),
        description=_(u"help_scrape_processing_instructions",
            default="Removes any processing instructions.")
    )
   
    scrape_embedded = schema.Bool(
        title=_(u"scrape_embedded", 
            default=u"Removes embedded objects"),
        description=_(u"help_scrape_embedded",
            default="Removes any embedded objects (flash, iframes).")
    )

    scrape_frames = schema.Bool(
        title=_(u"scrape_frames", 
            default=u"Security: frame-related tags"),
        description=_(u"help_scrape_frames",
            default="Removes any frame-related tags")
    )
 
    scrape_forms = schema.Bool(
        title=_(u"scrape_forms", 
            default=u"RemovE form tags"),
        description=_(u"help_scrape_forms",
            default="Removes any form tags")
    )

    scrape_annoying_tags = schema.Bool(
        title=_(u"scrape_annoying_tags", 
            default=u"Annoying tags"),
        description=_(u"help_scrape_annoying_tags",
            default="Tags that aren't *wrong*, but are annoying. 'blink' and 'marquee'")
    )
 

    form.widget(scrape_remove_tags=DataGridFieldFactory)
    scrape_remove_tags = schema.List(
        title=_(u"scrape_remove_tags", 
            default=u"remove tags"),
        description=_(u"help_scrape_remove_tags",
            default="""A list of tags to remove. Only the tags will be removed,
                their content will get pulled up into the parent tag."""),
        value_type=DictRow(schema=IScrapeTags),
        required=False,
    )
    
    form.widget(scrape_kill_tags=DataGridFieldFactory)
    scrape_kill_tags = schema.List(
         title=_(u"scrape_kill_tags", 
            default=u"Kill tags"),
        description=_(u"help_scrape_kill_tags",
            default="""A list of tags to kill.  Killing also removes the tag's content,
                i.e. the whole subtree, not just the tag itself."""),
        value_type=DictRow(schema=IScrapeTags),
        required=False,
    )
    
    form.widget(scrape_allow_tags=DataGridFieldFactory)
    scrape_allow_tags = schema.List(
        title=_(u"scrape_allow_tags", 
            default=u"Allow tags"),
        description=_(u"help_scrape_allow_tags",
            default="A list of tags to include (default include all)."),
        value_type=DictRow(schema=IScrapeTags),
        required=False,
    )

    scrape_remove_unknown_tags = schema.Bool(
        title=_(u"scrape_remove_unknown_tags", 
            default=u"Security: Remove unkonwn"),
        description=_(u"help_scrape_remove_unknown_tags",
            default="Remove any tags that aren't standard parts of HTML.")
    )

    scrape_add_nofollow = schema.Bool(
        title=_(u"scrape_add_nofollow", 
            default=u"Nofollow links"),
        description=_(u"help_scrape_add_nofollow",
            default=""" If true, then any <a> tags will have ``rel="nofollow"`` added to them.""")
    )

    scrape_host_whitelist = schema.Tuple(
        title=_(u"scrape_host_whitelist", 
            default="URLs to allow"),
        description=_(u"help_scrape_host_whitelists",
            default=u"""A list or set of hosts.
                (also for content like 'object', 'link rel="stylesheet"', etc).
                Anything that passes this test will be shown, regardless of
                the value of (for instance) ``embedded``.
                Note that this parameter might not work as intended if you do not
                make the links absolute. Note that you may also need to set whitelist_tags."""),
        value_type=schema.URI(),
        required = False,
    )
    
    form.widget(scrape_whitelist_tags=DataGridFieldFactory)
    scrape_whitelist_tags = schema.List(
        title=_(u"scrape_whitelist_tags", 
            default=u"""A set of tags that can be included with `host_whitelist'"""),
        description=_(u"help_scrape_host_whitelist",
            default="""The default  normal is ``iframe`` and ``embed``; you may wish to
            include other tags like ``script``, or you may want to
            implement ``allow_embedded_url`` for more control.  Set to None to
            include all tags."""),
        value_type=DictRow(schema=IScrapeTags),
        required=False,
    )
     
                
alsoProvides(ILxmlSettings, IMedialogControlpanelSettingsProvider)
