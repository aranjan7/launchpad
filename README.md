# launchpad
Script to view, edit and create bugs in Launchpad


*To view/search bugs use ./show_bug.py*

```
>> ./show_bug.py --help
Usage: ./show_bug.py: bug-id(s) 
Show or search launchpad bug(s)


Options:
  -h, --help            show this help message and exit
  -d, --detail          Describe bug in detail.
  -b, --brief           Describe bug in brief.
  -p PROJECT, --projet=PROJECT
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
  --tagany              Bugs matching one of the tags
  --since=SINCE         Create since date: in yyyy-mm-dd format
  --before=BEFORE       Create before date: in yyyy-mm-dd format
  --modified=MODIFIED   Modified since date: in yyyy-mm-dd format

```

*To edit a bug use 'edit_bug.py'*

```
./edit_bug.py --help
Usage: ./edit_bug.py: bug-id 
Edit Launchpad bug with given ID.


Options:
  -h, --help            show this help message and exit
  -n, --dryrun          Describe what the script would do without doing it.
  -p PROJECT, --project=PROJECT
                        launchpad project to work on
  -e SERIES, --series=SERIES
                        Edit or create list series. default is 'all'
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
  --verbose             Print what you are doing

```

*To create bug use ./create_bug.py*

```
>>  ./create_bug.py --help
Usage: ./create_bug.py: bug-title -t [tags] 
Create launchpad bug(s)

Options:
  -h, --help            show this help message and exit
  -n, --dryrun          Describe what the script would do without doing it.
  -p PROJECT, --project=PROJECT
                        launchpad project to work on
  -e SERIES, --series=SERIES
                        Edit or create list series. default is 'all'
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
  --verbose             Print what you are doing
  --public              set bug as public
  --security            set bug as security vulnerability
  --file=FILE           bug description file


```
