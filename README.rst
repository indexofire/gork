-------------------
Gork Readme
-------------------

Gork is a full site project based on feincms and many other apps. You can
see the demo site on http://www.hzcdclabs.org

===================
Installation
===================

  1. install dependencies like rabbitmq, postgresql, nginx, etc.
  2. git clone https://github.com/indexofire/gork.git
  2. mkvirtualenv gork
  3. pip install -r requirements.txt
  4. cd gork/src
  5. python manage.py syncdb --settings=settings.gork.local (or 'server' if production )

===================
Configuration
===================

  1. workon gork
  2. cdvirtualenv && cd bin
  3. echo 'export env varible' > activate  # define by your self if in production
