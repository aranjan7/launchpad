# launchpad
Script to edit, view bugs in Launchpad

**To edit a bug use 'edit-bug' **

```
>> ./edit-bug --help
Usage: ./edit-bug: bug-id Edit Launchpad bug with given ID.


Options:
  -h, --help            show this help message and exit
  -n, --dryrun          Describe what the script would do without doing it.
  -p PROJECT, --project=PROJECT
                        launchpad project to work on
  -e SERIES, --series=SERIES
                        Edit the specified series. 'all' is valid
  -m MILESTONE, --milestone=MILESTONE
                        set milestone
  -a ASSIGNEE, --assignee=ASSIGNEE
                        assign to launchpad ID
  -s STATUS, --status=STATUS
                        set status of the bug
  -c COMMENT, --comment=COMMENT
                         Add comment to the bug
  -i IMPORTANCE, --importance=IMPORTANCE
                        assign importance to the bug
  --verbose             Run with printing what you are doing

```

**To view/search bugs use ./show-bug **

```
>> ./show-bug --help
Usage: ./show-bug: bug-id(s) Show or search launchpad bug(s)


Options:
  -h, --help            show this help message and exit
  -d, --detail          Describe bug in detail.
  -b, --brief           Describe bug in brief.
  -p PROJET, --projet=PROJET
                        Specify launchpad project.
  -e SERIES, --series=SERIES
                        show bugs with given series
  -m MILESTONE, --milestone=MILESTONE
                        show bugs with given milestone
  -a ASSIGNEE, --assignee=ASSIGNEE
                        show bug assigned to given id
  -s STATUS, --status=STATUS
                        show bug with given status in comma separated strings.
  -r REPORTER, --reporter=REPORTER
                        show bug with given reporter
  -t TAGS, --tags=TAGS  show bugs with given tag. list of comma separted tags
                        e.g.,             "analytics, quench"
  --notags=NOTAGS       show bug without given tag(s). list of comma separted
                        tags
  --tagany              Bugs matching any tag
  --since=SINCE         Create since date: in yyyy-mm-dd format
  --before=BEFORE       Create before date: in yyyy-mm-dd format
  --modified=MODIFIED   Modified since date: in yyyy-mm-dd format
```
