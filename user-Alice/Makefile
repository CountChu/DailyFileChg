test1:
	python ../file_chg.py -s

test2:
	python ../report_file_chg.py -c config.yaml -o output

test3:
	python ../today_report.py --cmd "python ../file_chg.py -s -c config-test.yaml" -o output

sup: 								# Supplement log
	python ../file_chg.py --ymd 20231025 > output/2023-10-25.txt
	python ../file_chg.py --ymd 20231026 > output/2023-10-26.txt

load:
	launchctl load DailyReportFileChg.plist

list:
	launchctl list | grep com.alice

remove:
	launchctl remove com.alice.DailyReportFileChg

