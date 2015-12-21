#!/usr/bin/env python
#
# Copyright (C) 2015, Juniper Networks
#
# Author: Ashish Ranjan
#
# Script to show juniperopenstack bugs on launchpad.
#

"""Show or search launchpad bug(s)
"""

import os
import sys

from optparse import OptionParser

from launchpadlib.launchpad import Launchpad


status_dict = {
'FIX_COMMITTED' : 'Fix Committed',
'FIX_RELEASED' : 'Fix Released',
'TRIAGED' : 'Triaged',
'PROGRESS' : 'In Progress',
'NEW' : 'New',
'INCOMPLETE' : 'Incomplete',
'CONFIRMED' : 'Confirmed',
'WONTFIX' : 'Won\'t Fix',
'OPINION' : 'Opinion',
'INVALID' : 'Invalid'
}

cachedir = "~/.launchpadlib/cache/"


def printf(format, *args):
    sys.stdout.write(format % args)

def match_task(task, options):
    """ Further grep the bugs for fields not supported by searchTask
    """
    if (options.series == 'none' or options.series == task.target.name):
        if (options.milestone is None or 
                (task.milestone is not None and 
                   task.milestone.name == options.milestone) or
                (options.milestone.lower() == "none" and task.milestone is None)):
            # Filter unassigned bugs if "-a unassigned" is specified in cli.
            if (options.assignee is None or 
                    options.assignee.lower() != "unassigned" or
                    task.assignee is None): 
                return True
    return False

#
# Print bug details
#
def show_bug(bug, options):
   """ Print information about the bug
   """

   if bug is None:
       return

   ''' To speedup in case of simple search print and return from here
   '''

   if (options.brief and options.milestone is None and 
           (options.assignee is None or options.assignee.lower() != "unassigned")):
       print 'Bug %s: %s' %(bug.id, bug.title) 
       return

   ps = 'Scope(s):'
   task_list = [i for i in bug.bug_tasks if match_task(i, options)]
   for task in task_list:
       ms_name = "none"
       assignee = "none"
       if task.milestone is not None:
          ms_name = task.milestone.name
       if task.assignee is not None:
          assignee = task.assignee.name

       ps += "Series: {0:25} Assigned: {1:15} Importance: {2:14}  \
             Milestone: {3:12} Status: {4:20} \n".format(
                                task.bug_target_name, assignee, 
                                task.importance, ms_name, task.status)

   if options.detail:
       # print audit trail
       i = 0
       ps += "\nActivities:"
       for act in bug.messages:
           if i is not 0:
               ps += "\n-------------------------------------------------------------------------------\n"
               ps += '[%d]: ' % i
               ps += act.owner_link.rsplit('/',1)[-1] + ": wrote on " + str(act.date_created) + ":  " + act.subject
               ps += '\n%s \n ' % act.content
           i += 1

   if not task_list:
      return

   print 'Bug %s: %s' %(bug.id, bug.title) 
   if options.brief:
       return

   print '[PRIVATE]' if bug.private else '[PUBLIC]', 
   print 'Tags: %s' %(bug.tags),
   print ' Date Created: %s' % (bug.date_created)

   print '\nDescription:\n%s\n' % (bug.description)

   if options.detail:
      print ps

   return 

#
# Search bugs
#
def get_buglist(launchpad, o):
    dist = launchpad.projects[o.project]
    if o.series is not 'none':
        lp_series = dist.getSeries(name=o.series)
        omit = False
    else:
        lp_series = dist
        omit = True

    vargs = {}

    if o.reporter is not None:
        try:
            vargs['bug_reporter'] = launchpad.people[o.reporter]
        except KeyError:
            print 'User %s not found' % (o.reporter)
            return []

    if o.assignee is not None:
        try:
           if o.assignee.lower() != "unassigned":
               vargs['assignee'] = launchpad.people[o.assignee]
        except KeyError:
           print 'User %s not found' % (o.assignee)
           return []

    if o.milestone is not None:
        # here if milestone is "none", search should match with
        # bugs where milestone is not set. However, it doesn't
        # work because of https://bugs.launchpad.net/launchpad/+bug/70709
        #
        vargs['milestone'] = dist.getMilestone(name=o.milestone)
        if (vargs['milestone'] is None and 
                o.milestone.lower() != "none"):
           print 'Milestone %s is invalid' % (o.milestone)
           return []

    if o.status is not None:
        #split into list remove leading spaces
        vargs['status'] = [j.strip() for j in o.status.split(",")]
        st_l = [ v for v in status_dict.values() ]
        if not (set(st_l) >= set(vargs['status'])):
            print 'Valid values for status field are %s' % (st_l)
            return []

    if o.tags is not None:
        vargs['tags'] = [j.strip() for j in o.tags.split(",")]
        vargs['tags_combinator'] = 'All'

    if o.notags is not None:
        vargs['tags'] += ['-'+j.strip() for j in o.notags.split(",")]
        vargs['tags_combinator'] = 'All'

    if o.tagany:
        vargs['tags_combinator'] = 'Any'

    if o.since is not None:
        vargs['created_since'] = o.since

    if o.before is not None:
        vargs['created_before'] = o.before

    if o.modified is not None:
        vargs['modified_since'] = o.modified

    bug_list = lp_series.searchTasks(omit_targeted=omit, **vargs)

    return bug_list

def main(args):
    usage = """%s: bug-id(s) \n%s""" % (sys.argv[0], __doc__)
    parser = OptionParser(usage=usage)

    parser.add_option(
            '-d', '--detail', action='store_true', 
            help='Describe bug in detail.')
    parser.add_option(
            '-b', '--brief', action='store_true', help='Describe bug in brief.')
    parser.add_option(
            '-p', '--projet', type='string', action='store', dest = 'project',
            default='juniperopenstack', help='Specify launchpad project.')
    parser.add_option(
            '-e', '--series', type="string", action="store", dest="series", 
            default="none", help='show bugs with given series')
    parser.add_option(
            '-m', '--milestone', type="string", action="store", 
            help='show bugs with given milestone')
    parser.add_option(
            '-a', '--assignee', type="string", action="store", 
            help='show bug assigned to given id')
    parser.add_option(
            '-s', '--status', type="string", action="store", 
            help='show bug with given status in comma separated strings.')
    parser.add_option(
            '-r', '--reporter', type="string", action="store", 
            help='show bug with given reporter')
    parser.add_option(
            '-t', '--tags', type="string", action="store", 
            help='show bugs with given tag. list of comma separted tags e.g., \
            "analytics, quench"')
    parser.add_option(
            '--notags', type="string", action="store", 
            help='show bug without given tag(s). list of comma separted tags')
    parser.add_option(
             '--tagany', action='store_true', help='Bugs matching one of the tags')
    parser.add_option(
             '--since', type="string", action="store", 
             help='Create since date: in yyyy-mm-dd format')
    parser.add_option(
             '--before', type="string", action="store", 
             help='Create before date: in yyyy-mm-dd format')
    parser.add_option(
             '--modified', type="string", action="store", 
             help='Modified since date: in yyyy-mm-dd format')
    """
    parser.add_option(
             '--edit', dest='edit_action', type="string", action="store", 
             help='execute ./edit_bug.py on the search result')
    """

    (options, args) = parser.parse_args(args=args)

    launchpad = Launchpad.login_with('hello-world', 'production')

    if len(args) == 1:
       bug_list = get_buglist(launchpad, options)
       if bug_list: 
           print 'Total bugs: %d (Count will not match total bugs displayed, if search criteria has -m = "none")' % \
                (bug_list._wadl_resource.representation['total_size'])
           for bug_t in bug_list:
               show_bug(bug_t.bug, options)
           """ Todo: support edit bug here. """
    else:
       for bug in args[1:]:
          show_bug(launchpad.bugs[bug], options)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[0:]))
