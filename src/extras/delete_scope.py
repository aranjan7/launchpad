#!/usr/bin/env python
#
# Copyright (C) 2015, Juniper Networks
#
# Author: Ashish Ranjan
#
# Script to delete scope (task) of a bug in launchpad
#
"""Edit Launchpad bug with given ID.
"""

__metaclass__ = type

import os
import sys
from optparse import OptionParser

from launchpadlib.errors import Unauthorized
from launchpadlib.launchpad import Launchpad

def delete_scope(bug, options):
   """ Delete the bug task """

   bugtasks = bug.bug_tasks
   for task in bugtasks:
       if task.target.name == options.series:
          if options.dryrun:
              print ("Deleting series %s for bug %d " % 
                      (task.bug_target_name.rsplit('/')[-1], bug.id))
              return True
          task.lp_delete()
          return True

   return False

def main(args):
    global launchpad 
    global dist 

    usage = """%s: bug-id %s""" % (sys.argv[0], __doc__)
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-n', '--dryrun', action='store_true',
        help='Describe what the script would do without doing it.')
    parser.add_option(
            '-p', '--project', type="string", action="store", dest="project",
            default="juniperopenstack", help="launchpad project to work on")
    parser.add_option(
            '-e', '--series', type="string", action="store", dest="series", 
            default="all", help="Edit or create series. default is 'all'")

    (options, args) = parser.parse_args(args=args)

    if len(args) < 2:
        parser.print_usage()
        return 1

    for bug_id in args[1:]:
        launchpad = Launchpad.login_with('delete_scope', 'production', version='devel')
        dist = launchpad.distributions[options.project]
        bug = launchpad.bugs[bug_id]
        if options.series is not None:
            delete_scope(bug, options)


if __name__ == '__main__':
    sys.exit(main(sys.argv[0:]))
