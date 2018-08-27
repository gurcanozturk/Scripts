# Delete mails from IMAP server by subject.
#
import imaplib
imap_server = "mail.acme.com"
imap_user   = "gurcanozturk"
imap_pass   = ""
subject     = "Delete Me"

box = imaplib.IMAP4_SSL(imap_server, 993)
box.login(imap_user, imap_pass)
box.select('Inbox')
typ, data = box.search(None,'(UNSEEN SUBJECT "%s")' % subject)
for num in data[0].split():
   print num
   box.store(num, '+FLAGS', '\\Deleted')
box.expunge()
box.close()
box.logout()
