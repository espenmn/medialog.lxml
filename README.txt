medialog.lxml
=======================

WARNING: This product contains a view that could be a security RISK!


About the views and behavior
============================

- This is very experimental. Please give feedback and suggestions.

- The embed views are probably insecure, if the remote site contains evil code.



How to embed another webpage in your site
=========================================

- go to control panel.

- in the medialog.control panel, set *default settings for your embed views*

- add a dexterity content type

- add  LXML embed behaviour 

- Add a content type to your site and enter embed details

- go to http://plonesite/content/scrape_view 

- You probably want to add the view to the contenttype TTW



How add content from another webpage in your site
=================================================

- be sure to set up whitelist and url pairs in the control panel
- go to a folder
- add /@@createpage?url=http://url/of/somepage
- go to your folder: a new page should have been added 
- PS: Settings in the medialog control panel and html safe settings are taken into account


 
The view
========

http://yoursite.com/scrape?url=http://plone.org/products/plone/features/


Author
======

Espen Moe-Nilssen, Grieg Medialog AS


