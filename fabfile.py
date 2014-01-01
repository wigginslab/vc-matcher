from fabric.api import *
import os

# the user to use for the remote commands
env.user = os.getenv('prod_user')
# the servers where the commands are executed
env.hosts = [os.getenv('prod_host')]

def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/vc-matcher.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir /tmp/vc-matcher')
    with cd('/tmp/vc-matcher'):
        run('tar xzf /tmp/vc-matcher.tar.gz')
        # now setup the package with our virtual environment's
        # python interpreter
        run('/var/www/vc-matcher/env/bin/python setup.py install')
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/vc-matcher /tmp/vc-matcher.tar.gz')
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    run('touch /var/www/vc-matcher.wsgi')