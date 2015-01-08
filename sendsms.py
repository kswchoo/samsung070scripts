#!/usr/bin/python
# -*- coding: utf-8 -*-

import url, urllib, urllib2, cookielib, hashlib, sys

username = 'username'
password = 'passw0rd'
mynumber = '07012345678'

if (len(sys.argv) == 4):
	sender = sys.argv[3]
else:
	sender = mynumber

message=sys.argv[2]
receiver=sys.argv[1]
passwordhash = hashlib.sha1(password).hexdigest()

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko')]

login_data = urllib.urlencode({'loginId' : username, 'decryptedPwd' : password, 'password' : passwordhash, 'method' : 'login'})
resp = opener.open('http://www.samsung070.com/LoginAction.do', login_data)
response = unicode(resp.read(), 'euc-kr')
if not u"환영 합니다" in response:
	print "Login failed"
	sys.exit(-1)

opener.addheaders = [('Referer', 'http://www.samsung070.com/user_forward.do?forward_name=additionServiceMain')]
resp = opener.open('http://www.samsung070.com/user_additionservice_main.do')
response = unicode(resp.read(), 'euc-kr')
if not "/iphon_user_sms_info.do?selectedRqUserId=" + mynumber + "&code=00" in response:
	print mynumber + " seems not your number."
	sys.exit(-2)

opener.addheaders = [('Referer', 'http://www.samsung070.com/iphone_sms_small.do?selectedRqUserId=' + mynumber)]
resp = opener.open('https://www.samsung070.com/iphone_sms_small.do?selectedRqUserId=' + mynumber)
response = unicode(resp.read(), 'euc-kr')
if not "value=\"" + mynumber + "\"" in response:
	print mynumber + " seems not your number."
	sys.exit(-3)


sms_data = urllib.urlencode({'message1': message.decode('utf-8').encode('euc-kr'),
	                         'receivers': receiver,
	                         'receiver': receiver,
	                         'receiverOrg': receiver,
	                         'sender': sender})
resp = opener.open('http://www.samsung070.com/iphone_sms_small_send.do', sms_data)
response = unicode(resp.read(), 'euc-kr')
if not u"메시지 전송요청이 완료되었습니다" in response:
	print "SMS send failed"
	sys.exit(-4)

