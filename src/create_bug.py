#!/usr/bin/env python
#
# Copyright (C) 2015, Juniper Networks
#
# Author: Ashish Ranjan
#
# Script to create juniperopenstack bugs on launchpad.
#

""" Create launchpad bug(s)
"""
import os
import sys
import edit_bug

from optparse import OptionParser

from launchpadlib.launchpad import Launchpad

importance_dict = {
    'UNKNOWN' : 'Unknown',
    'UNDECIDED' : 'Undecided',
    'CRITICAL' : 'Critical',
    'HIGH' : 'High',
    'MEDIUM' : 'Medium',
    'LOW' : 'Low',
    'WISHLIST' : 'Wishlist'
}

def get_bug_descr(options):
    desc = ""
    if options.file is not None:
        with open('options.file', 'r') as myfile:
            if not myfile:
               print "File %s not found" % options.file
            else:
               desc = myfile.read()
        return desc

    if options.stdin:
       for line in sys.stdin:
           desc += line
       return desc

    print "Enter bug detail. End with '.': "
    while True:
       in_str = raw_input("")
       if in_str == "." or not in_str: 
           break
       else:
           desc += in_str + '\n'
    return desc

def main(args):
    usage = """%s:  title %s -t [tags]""" % (sys.argv[0], __doc__)
    parser = OptionParser(usage=usage)

    parser.add_option(
            '-p', '--projet', type='string', action='store', 
            default='juniperopenstack', help='Specify launchpad project.')
    parser.add_option(
            '-e', '--series', type="string", action="store", 
            default="all", help="set the scope on which bug was found ")
    parser.add_option(
            '-a', '--assignee', type="string", action="store", 
            help='bug assigned to')
    parser.add_option( '-t', '--tags', type="string", action="store", 
            help='space separated list of tags')
    parser.add_option('-i', '--importance', type="string", action="store", 
            help='set importance of the bug')
    parser.add_option('--public', action="store_true", 
            help='set bug as public')
    parser.add_option('--security', action="store_true", 
            help='set bug as security vulnerability')
    parser.add_option('--file', action="store", help='get bug description from file')
    #parser.add_option('-', dest='stdin', action="store_true", 
            #help='get bug description from stdin')
    parser.add_option(
            '-s', '--status', type="string", action="store", 
            help="set status of the bug")

    (options, args) = parser.parse_args(args=args)
    if (len(args) < 2):
        parser.print_usage()

    if options.importance is not None:
        imp = [j.strip() for j in options.importance.split(",")]
        imp_l = [ v for v in importance_dict.values() ]
        if not (set(imp_l) >= set(imp)):
            print 'Valid values for importance field are %s' % (imp_l)
            return []

    if options.tags is None:
        print 'Error: specify at least 1 tag'
        return

    bug_title = args[1]
    setattr(options, "stdin", False)
    if len(args) == 3 and args[2] == "-":
       setattr(options, "stdin", True)

    bug_desc = get_bug_descr(options)
    print "Description: \n%s " % bug_desc
    return 0
   
    itype = "Private"
    if options.public:
        itype = "Public"

    launchpad = Launchpad.login_with('create_bug', 'production')
    dist = launchpad.distributions[options.project]

    if options.series is not None:
        series = dist.getSeries(name=options.series)
        if series is None:
            print "series %s is invalid" % options.series
            return -1

    bug = launchpad.bugs.createBug(description=bug_desc, tags=options.tags, 
            information_type = itype, security_related = options.security,
            title = bug_title, target = dist)

    if bug is None:
        print "Error creating bug"
        return -1

    nseries = dist.getSeries(name="trunk")
    if nseries is not None:
        new_task = bug.addTask(target=nseries)
        edit_series(task=new_task, options=options)

    new_task = bug.addTask(target=series)
    edit_series(task=new_task, options=options)
        
    print "Created bug %d" % bug.id
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[0:]))
