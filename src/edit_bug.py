#!/usr/bin/env python
#
# Copyright (C) 2015, Juniper Networks
#
# Author: Ashish Ranjan
#
# Script to scrub Contrail bugs on launchpad.
#
"""Edit Launchpad bug with given ID.
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

importance_dict = {
    'UNKNOWN' : 'Unknown',
    'UNDECIDED' : 'Undecided',
    'CRITICAL' : 'Critical',
    'HIGH' : 'High',
    'MEDIUM' : 'Medium',
    'LOW' : 'Low',
    'WISHLIST' : 'Wishlist'
}

cachedir = "~/.launchpadlib/cache/"
launchpad = None
dist = None

#
# Get matching object from the milestone collection in series
#
def get_milestone(ser, milestone_str):
    if (milestone_str is None or ser is None):
        return None

    if 'trunk' in str(ser):
        allms = dist.active_milestones
        for ms in allms:
           if milestone_str in str(ms):
               return ms
        return None
        
    if milestone_str.lower() == "latest":
        return ser.all_milestones[0]

    for ms in ser.all_milestones:
        if milestone_str in str(ms):
            return ms

    return None

#
# add a series to a given bug with assignee, milestone fields set
#
def edit_series(task, milestone, options):

    if options.assignee is not None:
        assignee = launchpad.people[options.assignee]
        if assignee is None:
            print 'Error: Invalid assignee %s' % (options.assignee)
    else:
        assignee = None

    if milestone is not None:
        task.milestone_link = milestone

    if options.status is not None:
        task.status = options.status

    if assignee is not None:
        task.assignee = assignee

    if options.importance is not None:
        task.importance = options.importance

    if options.dryrun or options.verbose:
        print("Bug: %s series: %s milestone: %s assignee: %s status: %s importance: %s" % 
            (task.bug_link.rsplit('/',1)[-1], task.target.name,
             str(task.milestone_link).rsplit('/',1)[-1], task.assignee.name, 
             task.status, task.importance))

    if not options.dryrun:
        task.lp_save()

    return

def edit_bug(bug, options):
   """ Function to set milestone to existing series (aka 'task') in the bug

   If the specified series is not linked to the bug, link it and set
   'assignee' & 'importance' field from other existing series
   """

   importance = options.importance
   milestone = options.milestone
   trunk_present = False
   bugtasks = bug.bug_tasks

   for task in bugtasks:
       # 
       # Launchpad doesn't like it if you edit both default and 
       # 'trunk' series so skip trunk
       #
       if ((options.series == "all" ) or 
               task.target.name == options.series):

           task_name = task.target.name
           if (task_name == 'trunk'):
               trunk_present = True

           series = dist.getSeries(name=task_name)
           if not series:
               continue

           milestone_link = get_milestone(ser=series, milestone_str=milestone)

           edit_series(task, milestone_link, options)
           if options.series != "all":
               return True

           if not milestone_link and milestone is not None and series:
               print "Milestone %s not found for series %s " % \
                    (milestone, series)

   # We come here in case of -e = all or we need to create new bug task
   # In above loop we never edit the base task. We create a 'trunk'
   # task as a to track the bug status as a policy.
   series = None
   if (options.series == 'all' and not trunk_present):
       series = dist.getSeries(name="trunk")

   if (options.series != "all" or not trunk_present):
      #create the missing series 
      if series is None:
          series = dist.getSeries(name=options.series)
      new_task = bug.addTask(target=series)
      milestone_link = get_milestone(ser=series, milestone_str=milestone)
      edit_series(new_task, milestone_link, options)

   return False

def set_comment(bug, comment):
   bug.newMessage(content=comment)
   bug.lp_save()
   return
       

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
    parser.add_option(
            '-m', '--milestone', type="string", action="store", 
            dest="milestone",  help="set milestone")
    parser.add_option(
            '-a', '--assignee', type="string", action="store", dest="assignee", 
            help="assign to launchpad ID")
    parser.add_option(
            '-s', '--status', type="string", action="store", dest="status",
            help="set status of the bug")
    parser.add_option(
            '-c', '--comment', type="string", action="store", dest="comment", 
            help=" Add comment to the bug")
    parser.add_option(
            '-i', '--importance', type="string", action="store", 
            dest="importance", help="assign importance to the bug")
    parser.add_option(
         '--verbose', action='store_true', help='Print what you are doing')

    (options, args) = parser.parse_args(args=args)

    if len(args) < 2:
        parser.print_usage()
        return 1

    if options.status is not None:
        #split into list remove leading spaces
        status = [j.strip() for j in options.status.split(",")]
        st_l = [ v for v in status_dict.values() ]
        if not (set(st_l) >= set(status)):
            print 'Valid values for Status field are %s' % (st_l)
            return []

    if options.importance is not None:
        imp = [j.strip() for j in options.importance.split(",")]
        imp_l = [ v for v in importance_dict.values() ]
        if not (set(imp_l) >= set(imp)):
            print 'Valid values for importance field are %s' % (imp_l)
            return []

    launchpad = Launchpad.login_with('hello-world', 'production')
    dist = launchpad.distributions[options.project]
    for bug_id in args[1:]:
        bug = launchpad.bugs[bug_id]

        if options.comment is not None:
            set_comment(bug, options.comment)
        
        # Find series object
        if options.series is not None:
            edit_bug(bug, options)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[0:]))
