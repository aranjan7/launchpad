#!/usr/bin/env python
#
# Copyright (C) 2015, Juniper Networks
#
# Author: Ashish Ranjan
#
# Script to create juniperopenstack bugs on launchpad.
#

"""Create launchpad bug(s)
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

    usage = """%s: <bug-title> -t [tags] \n%s""" % (sys.argv[0], __doc__)
    parser = OptionParser(usage=usage)

    edit_bug.opt_parser_init(parser)

    parser.add_option('--security', action="store_true", 
            help='set bug as security vulnerability')
    parser.add_option('--file', action="store", 
            help='bug description file')

    (options, args) = parser.parse_args(args=args)
    if (len(args) < 2):
        parser.print_usage()
        return 1

    if options.importance is not None:
        imp = [j.strip() for j in options.importance.split(",")]
        imp_l = [ v for v in importance_dict.values() ]
        if not (set(imp_l) >= set(imp)):
            print 'Valid values for importance field are %s' % (imp_l)
            return []

    if options.tags is None:
        print 'Error: must specify at least 1 tag'
        return

    bug_title = args[1]
    setattr(options, "stdin", False)
    if len(args) == 3 and args[2] == "-":
       setattr(options, "stdin", True)

    bug_desc = get_bug_descr(options)
   
    itype = "Private"
    if options.public:
        itype = "Public"

    edit_bug.launchpad = Launchpad.login_with('create_bug', 'production')
    edit_bug.dist = edit_bug.launchpad.distributions[options.project]

    series_list = [j.strip() for j in options.series.split(" ")]
    if 'all' not in series_list:
        if 'trunk' not in series_list:
            options.series += " trunk"
        
    if options.dryrun or options.verbose:
       print "Creating %s bug Title: %s\n" % (itype, bug_title)
       print "Tags: %s" % options.tags
       print "Description %s\n" % bug_desc

    if options.dryrun:
       return 0

    bug = edit_bug.launchpad.bugs.createBug(description=bug_desc, 
            tags=options.tags, information_type = itype, 
            security_related = options.security, title = bug_title, 
            target = edit_bug.dist)

    if bug is None:
        print "Error creating bug"
        return -1

    edit_bug.edit_bug(bug, options)

    print "Created bug %d" % bug.id
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[0:]))
