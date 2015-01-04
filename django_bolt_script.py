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


def create_project(project_path_name, template_path='abalt-template.zip', user_name='', user_email=''):
    """
    Generate new django project using a custom template, also initialize a
    new git repo with all non-ignored files commited as "Init commit".

        Note:
            - Script assume that you have git and django already installed.

    """
    from os import chdir, path, walk, mkdir, system
    from subprocess import call
    from zipfile import ZipFile

    # if template_path is relative then must be found in the same directory
    if template_path == path.basename(template_path):
        template_path = path.join(path.dirname(__file__), template_path)
    
    if not path.exists(template_path):
        raise Exception("Template path couldn't been found")    
    
    project_name = path.basename(project_path_name)
    if not project_name:
        raise Exception("Must provide a project name or folder")        
    
    # if project_path_name is relative then use script path
    if project_name == project_path_name:
        project_path_name = path.join(path.curdir, project_path_name)
    
    if not path.exists(project_path_name):
        mkdir(project_path_name)

    chdir(project_path_name)
        
    # Create Django project using custom template.
    system('django-admin startproject %s --template=%s --extension=py,rst,html' % (project_name, template_path))

    # Go inside created django project
    chdir(path.join(path.curdir, project_name))

    # Start Git repository
    call(['git', 'init'])

    # if provided user name and email use it on git, else use global.
    if user_name and user_email:
        call(['git', 'config',  'user.name', user_name])
        call(['git', 'config',  'user.email', user_email])
    call(['git', 'add', '-A'])
    call(['git', 'commit', '-m', 'Initial commit\n\nProject generated with django_bolt_script (http://github.com/ecairo/django_bolt)'])

    chdir(path.pardir)

    # Zip whole django project
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
        if args_count == 5:
            create_project(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        elif args_count == 3:
            create_project(sys.argv[1], sys.argv[2])
        elif args_count == 2:
            create_project(sys.argv[1])
        else:
            print '-------'
            print 'usage 1: django_bolt_script.py project_name'
            print 'usage 2: django_bolt_script.py project_name project_template'
            print 'usage 3: django_bolt_script.py project_name project_template user_name user_email'
    except Exception, e:
        print e.message
        raw_input()
