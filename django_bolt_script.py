#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Script to boiler plate a django project using a custom template,
also initialize a git repository for it.

Requirements:
    - Installed Git
    - Installed Django
"""

__author__ = 'Ernesto Perez Cairo'
__author_email__ = 'ecairo@abalt.org'


def create_project(project_name, user_name='', user_email='',
                   template_path='abalt-template.zip'):
    """
    Generate new django project using a custom template, also initialize a
    new git repo with all non-ignored files commited as "Init commit".

        Note:
            - Script assume that you have git and django already installed.

    """
    from os import chdir, path, walk, mkdir, system
    from subprocess import call
    from zipfile import ZipFile

    if not path.exists(project_name):
        mkdir('./%s' % project_name)
    chdir('./%s' % project_name)

    # Create Django project using custom template.
    system('django-admin.py startproject %s --template=../%s --extension=py,rst,html' % (project_name, template_path))

    chdir('./%s' % project_name)

    # Git
    call(['git', 'init'])

    # If provided user name and email use it on git, else use global.
    if user_name and user_email:
        call(['git', 'config',  'user.name', user_name])
        call(['git', 'config',  'user.email', user_email])
    call(['git', 'add', '-A'])
    call(['git', 'commit', '-m', 'Initial commit\n\nProject generated with django_bolt_script (http://github.com/ecairo/django_bolt)'])

    chdir('..')

    # Zip whole project
    zf = ZipFile("%s.zip" % project_name, "w")
    for dirname, subdirs, files in walk(project_name):
        zf.write(dirname)
        for filename in files:
            zf.write(path.join(dirname, filename))
    zf.close()

if __name__ == '__main__':
    import sys
    try:
        args_count = len(sys.argv)
        if args_count == 4:
            create_project(sys.argv[1], sys.argv[2], sys.argv[3])
        elif args_count == 2:
            create_project(sys.argv[1])
        else:
            print '-------'
            print 'usage 1: django_bolt_script.py project_name'
            print 'usage 2: django_bolt_script.py project_name user_name user_email'
    except Exception, e:
        print e.message
