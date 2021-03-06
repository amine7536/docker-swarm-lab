# -*- coding: utf-8 -*-

from json import dumps
from .base import Module
from .utils import logger, read_json_file
from os import path, environ, chdir, getcwd, execle, execl
from .utils.decorators import register_action
from .base import Module, ModuleRuntimeError


class Hello(Module):
    """
    Hello Module
    """

    def __init__(self, options, *args, **kwargs):
        """
        Init Applications Module
        """
        super(Hello, self).__init__(options, *args, **kwargs)
        self.options = options
        self.svc = self.options.get('<svc_name>')
        self.branch = self.options.get('--branch')
        self.deps = self.options.get('--deps')
        
        self.Dockerfile = "/vagrant/%s/Dockerfile" % self.svc
        self.Configfile = "/vagrant/%s/config.json" % self.svc
        self.Repo ="/vagrant/%s" % self.svc
        self.Tag ="%s-%s" % (self.svc, self.branch)
        self.Name = "%s-%s" % (self.branch, self.svc)
        self.ServiceDomain = "%s.pix.lab" % self.Name
        self.ID = 1
        
        # Cheating - should be in a configuration file
        # Dependencies between Services should be in ETCD or CONSUL
        if self.svc == "ms1":
            self.ID = 2
        # Cheating - should be in a configuration file
        # Dependencies between Services should be in ETCD or CONSUL

    @register_action('build')
    def build_svc(self):
        """
        Build Service from a repo
        """
        logger.info("Pushing feature branch: %s for Service: %s" % (self.branch, self.svc))
        logger.info("Building docker image %s:%s" %(self.svc, self.branch))
        logger.info("Checkout branch %s" %self.branch)
        logger.info("Using Dockerfile /vagrant/%s/Dockerfile" % self.svc)

        try:
            #TODO: should ask for sudo
            execl("/usr/bin/sudo", "", "docker",  "build", self.Repo, "-f", self.Dockerfile, "-t",  self.Tag)
        except Exception as e:
                raise SystemExit("Exepction: %s" % e)
        else:
            raise ModuleRuntimeError("Build failed")

        print 'You supplied the following options:', dumps(self.options, indent=2, sort_keys=True)

    
    @register_action('run')
    def run_service(self):
        """
        Start a Service
        """
        logger.info("Running feature branch: %s for Service: %s" % (self.branch, self.svc))
    
        print self.Dockerfile
        print self.Repo
        print self.Tag
        print self.Name
        print self.ServiceDomain

        if  not self.deps:
            raise ModuleRuntimeError("Please specify service dependecies with --deps")
        else:
            msUrl = "MS_URL=http://%s-%s.pix.lab" % (self.branch, self.deps)

        try:
            #TODO: should asj for sudo
            execl("/usr/bin/sudo", "", "docker", "service", "create", "--name", self.Name, 
            "-e" , "RACK_ENV=production", 
            "-e", msUrl,
             "--network", "apps", 
             "--network", "proxy", 
             "--label", "com.df.notify=true", 
             "--label", "com.df.distribute=true", 
             "--label", "com.df.serviceDomain=%s" % self.ServiceDomain, 
             "--label", "com.df.port=3000",
              self.Tag)
        except Exception as e:
                raise SystemExit("Exepction: %s" % e)
        else:
            raise ModuleRuntimeError("Build failed")