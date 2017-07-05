# -*- coding: utf-8 -*-

import re
import ssl
from json import dumps
from os import path, environ, chdir, getcwd, execle, execl
from .base import Module, ModuleRuntimeError
from .utils import register_action, logger, render_template, write_file, validate_params
from .utils import make_dir, user_input, user_confirm, read_json_file, create_sym_link


class Applications(Module):
    """
    Applications Module
    """

    def __init__(self, options, *args, **kwargs):
        """
        Init Applications Module
        """
        super(Applications, self).__init__(options, *args, **kwargs)
        self.options = options
        self.svc = self.options.get('<svc>')
        self.branch = self.options.get('--branch')
        self.Dockerfile = "/vagrant/%s/Dockerfile" % self.svc
        self.Repo ="/vagrant/%s" % self.svc
        self.Tag ="%s:%s" % (self.svc, self.branch)
        self.Name = "%s-%s" % (self.branch, self.svc)
        self.ServiceDomain = "%s.pix.lab" % self.Name


    #######################
    # Module Actions      #
    #######################

    @register_action('help')
    def module_help(self):
        print("""Applications Module
        Actions : create, run
        Options:
            --name=<name> [Default: John ]
        """)
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

        if self.app_name is not None:
            self.config_file = self.resolve_config(self.options.get('--config'))

    @register_action('build')
    def create_app(self):
        logger.info("Pushing feature branch: %s for Service: %s" % (self.branch, self.svc))
        logger.info("Building docker image %s:%s" %(self.svc, self.branch))
        logger.info("Checkout branch %s" %self.branch)
        logger.info("Using Dockerfile /vagrant/%s/Dockerfile" % self.svc)

        try:
            #TODO: should asj for sudo
            execl("/usr/bin/sudo", "", "docker",  "build", self.Repo, "-f", self.Dockerfile, "-t",  self.Tag)
        except Exception as e:
                raise SystemExit("Exepction: %s" % e)
        else:
            raise ModuleRuntimeError("Build failed")

    
    @register_action('run')
    def create_app(self):
        logger.info("Running feature branch: %s for Service: %s" % (self.branch, self.svc))
    
        print self.Dockerfile
        print self.Repo
        print self.Tag
        print self.Name
        print self.ServiceDomain

        runCmd = """
        docker service create --name %s \
            -e MS_URL=http://new-branch-ms2.pix.lab \
            --network apps \
            --network proxy \
            --label com.df.notify=true \
            --label com.df.distribute=true \
            --label com.df.servicePath=/  \
            --label com.df.serviceDomain=%s \
            --label com.df.port=8080 \
            %s
        """ % (self.Name, self.ServiceDomain, self.Tag)

        print runCmd

        try:
            #TODO: should asj for sudo
            execl("/usr/bin/sudo", "", runCmd)
        except Exception as e:
                raise SystemExit("Exepction: %s" % e)
        else:
            raise ModuleRuntimeError("Build failed")
