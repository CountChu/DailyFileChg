# DailyFileChg
The project provides python applications to list files that were updated or created on a certain day, and also provides scripts to daily report file changes.

# Applications

## file_chg.py

Usage 1: Display changes of files and directories today.
```
    python file_chg.py
```

Usage 2: Display fchanges of files and directories on 2022/2/21
```
    python file_chg.py --ymd 20220221
```

Usage 3: Display changes of files and directories today in silience mode.
```
    python file_chg.py -s
```

Usage 4: Display changes of files and directories today by a given YAML config.
```
    python file_chg.py -c config-YOUR-NAME.yaml	
```

Usage 5: Display changes of only files.
```
    python file_chg.py --only-files
```

## today_report.py
The app saves a report from a given command in a file named with today's date, E.g., 2023-10-30.txt.

Usage 1: Report the command "python file_chg.py -s" in a today's file of output directory.
```
    python today_report.py -cmd "python file_chg.py -s" -o output
```

