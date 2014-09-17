medialog.lxml
=======================

WARNING: This product contains a view that could be a security RISK!

https://www.youtube.com/watch?v=jE1gLOBBKb4


About the views and behavior
============================

- This is slightly experimental. Please give feedback and suggestions.

- The embed views might be insecure, although if you are restrictive with the settings in the control panel you should be able to filter out evil code.



How to embed another webpage to your site
=========================================

- go to the control panel.

- in the medialog.control panel, set *default settings for your embed views*

- add a dexterity content type

- add LXML embed behaviour 

- Add a content type to your site and enter embed details

- go to http://plonesite/content/scrape_view 

- You probably want to add the view to the contenttype TTW



How add content from another webpage to your site
=================================================

- be sure to set up whitelist and url pairs in the control panel
- go to a folder
- add /@@createpage?url=http://url/of/somepage
- go to your folder: a new page should have been added 
- PS: Settings in the medialog control panel and html safe settings are taken into account


How batch add content from other webpages to your site
=======================================================

- make a CSV file with ‘url’ and ‘selector’ rows
- go to a folder
- add /@@createpages
- select the CSV file
- A page for each corresponding url & selector will be added
- In other words, if you add a line with http://plone.org and #content-core, a Page will be added to your site and the body text will be that of #content-core from plone.org’s front page.

 
The view
========

http://yoursite.com/scrape?url=http://plone.org/products/plone/features/


Author
======

Espen Moe-Nilssen, Grieg Medialog AS


