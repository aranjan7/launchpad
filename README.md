# launchpad
Script to edit, view bugs in Launchpad


Usage: ./edit-bug: bug-id 

None

Options:
  -h, --help            show this help message and exit
  -n, --dry-run         Describe what the script would do without doing it.
  -m MILESTONE, --milestone=MILESTONE
                        set milestone
  -e SERIES, --series=SERIES
                        Edit series
  --newseries=NEWSERIES
                        create new series
  -a ASSIGNEE, --assignee=ASSIGNEE
                        assign to launchpad ID
  -s STATUS, --status=STATUS
                        set status of the bug
  -c COMMENT, --comment=COMMENT
                         Add comment to the bug
  -i IMPORTANCE, --importance=IMPORTANCE
                        assign importance to the bug


Usage: ./show-bug: bug-id 
Show launchpad bug
   


Options:
  -h, --help            show this help message and exit
  -d, --detail          Describe bug in detail.
  -b, --brief           Describe bug in brief.
  -m MILESTONE, --milestone=MILESTONE
                        show bugs with given milestone
  -e SERIES, --series=SERIES
                        show bugs with given series
  -a ASSIGNEE, --assignee=ASSIGNEE
                        show bug assigned to given id
  -s STATUS, --status=STATUS
                        show bug with given status. list of comma separated
                        status strings.
  -r REPORTER, --reporter=REPORTER
                        show bug with given reporter
  -t TAGS, --tags=TAGS  show bugs with given tag. tag or list of comma
                        separted tags e.g., "analytics, quench"
  --notags=NOTAGS       show bug without given tag(s). tag or list of comma
                        separted tags e.g., "blocker, quench"
  --tagany              Bugs matching any tag
  --since=SINCE         Create since date: in yyyy-mm-dd format
  --before=BEFORE       Create before date: in yyyy-mm-dd format
  --modified=MODIFIED   Modified since date: in yyyy-mm-dd format

