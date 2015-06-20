# move_trash_to_archive
Simple python script to log into IMAP server and move messages from Trash to Archive

This can be useful for instance if you use a simple/limited IMAP client to access GMail or similar service and the simple client does not conform to the rules for moving files.

I use this with a Jenkins job or cronjob to ensure my mail is cleaned up regularly - here is the cronjob (every 15 minutes):
````
15 * * * *  /home/username/apps/gmail_undeleter/move_trash_to_archive.py
````

Run 
````
crontab -e
````
to edit/insert the cronjob and make sure to have a trailing newline.
