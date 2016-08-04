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
    elif options.milestone and options.milestone.lower() == "null":
        task.milestone_link = None
        
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

def add_comment_tag(bug, options):
   if options.comment is not None:
      bug.newMessage(content=options.comment)
   if options.tags is not None:
      tag_list = [j.strip() for j in options.tags.split(" ")]
      bug.tags = tag_list
   if options.public is not None:
      bug.private = False

   bug.lp_save()
   return

def edit_bug_tasks(bug, options):
   """ Function to set milestone etc to existing task(s)

   If the specified series is not linked to the bug, link it and set
   'assignee' & 'importance' field from other existing series
   """

   importance = options.importance
   milestone = options.milestone
   trunk_present = False
   bugtasks = bug.bug_tasks

   series_list = [j.strip() for j in options.series.split(" ")]

   for task in bugtasks:
       # 
       # Launchpad doesn't like it if you edit both default and 
       # 'trunk' series so skip trunk
       #
       task_name = task.target.name
       if ("all" in series_list or 
               task.target.name in series_list):

           if (task_name == 'trunk'):
               trunk_present = True

           series = dist.getSeries(name=task_name)
           if not series:
               continue

           milestone_link = get_milestone(ser=series, milestone_str=milestone)

           edit_series(task, milestone_link, options)
           try:
               series_list.remove(task_name)
           except ValueError:
               pass

           if not series_list:
               return True

           if not milestone_link and milestone is not None and series:
               print "Milestone %s not found for series %s " % \
                    (milestone, series)

       if (task_name == options.project or task_name == 'trunk'):
           if options.assignee is None and task.assignee:
               options.assignee = task.assignee.name
           if options.importance is None:
               options.importance = task.importance 


   # We come here in case of -e = all or we need to create new bug task
   # In above loop we never edit the base task. We create a 'trunk'
   # task as a to track the bug status as a policy.
   if "all" in series_list: 
       if not trunk_present:
          series_list.append("trunk")
       series_list.remove("all")

   # Create remaining scope aka task
   for series_name in series_list:
      series = dist.getSeries(name=series_name)
      if series is None:
          continue
      new_task = bug.addTask(target=series)
      milestone_link = get_milestone(ser=series, milestone_str=milestone)
      edit_series(new_task, milestone_link, options)

   return False

def edit_bug(bug, options):
    edit_bug_tasks(bug, options)
    if options.comment or options.tags or options.public:
       add_comment_tag(bug, options)
    return
    
def opt_parser_init(parser):
    parser.add_option(
        '-n', '--dryrun', action='store_true',
        help='Describe what the script would do without doing it.')
    parser.add_option(
            '-p', '--project', type="string", action="store", dest="project",
            default="juniperopenstack", help="launchpad project to work on")
    parser.add_option(
            '-e', '--series', type="string", action="store", dest="series", 
            default="all", help="Edit or create list series. default is 'all'")
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
    parser.add_option('-t', '--tags', type="string", action="store", 
                         help='space separated list of tags')
    parser.add_option('--public', action="store_true", help='set bug as public')
    parser.add_option(
         '--verbose', action='store_true', help='Print what you are doing')

    return

def main(args):
    global launchpad 
    global dist 

    usage = """%s: bug-id \n%s""" % (sys.argv[0], __doc__)
    parser = OptionParser(usage=usage)
    opt_parser_init(parser)
    
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

    launchpad = Launchpad.login_with('edit_bug.py', 'production')
    dist = launchpad.distributions[options.project]
    for bug_id in args[1:]:
        bug = launchpad.bugs[bug_id]

        edit_bug(bug, options)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[0:]))
