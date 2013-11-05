#!/usr/bin/python

"""
groupadd -g 10002 ldap_test

ldapsearch -x -H ldap://172.16.2.201 -D cn=ldap,cn=users,dc=gm,dc=local -w ldap -b
 CN=ldap_test,CN=Users,DC=gm,DC=local
"""

import os
import sys
import pwd
import grp
import ldap

def findgroup(group_id):
    # Load all of the user data, sorted by username
    all_groups = grp.getgrall()
    interesting_groups = sorted((g for g in all_groups if not g.gr_name.startswith('_')), key=operator.attrgetter('gr_name'))
    
    # Print the data
    for g in interesting_groups:
		if g.gr_gid == group_id
            print fmt % (name_length, g.gr_name, g.gr_gid, g.gr_passwd, ', '.join(g.gr_mem))
            return true
            
    return false
    
# Find the longest length for the name
"""name_length = max(len(g.gr_name) for g in interesting_groups) + 1

# Print report headers
fmt = '%-*s %4s %10s %s'
print fmt % (name_length, 'Name', 
             'GID', 
             'Password',
             'Members')
print '-' * name_length, '----', '-' * 10, '-' * 30

# Print the data
for g in interesting_groups:
    print fmt % (name_length, g.gr_name, 
                 g.gr_gid, 
                 g.gr_passwd,
                 ', '.join(g.gr_mem))
"""

def finduser(user):
	try:
		pwd.getpwnam(user)
		print user, "user exists"
		return True
	except:
		return False

def search_member_in_ldap(ldap, ldapo, cn):
	baseDN = cn
	#"dc=gm,dc=local"
	searchScope = ldap.SCOPE_SUBTREE
	## retrieve all attributes - again adjust to your needs - see documentation for more options
	retrieveAttributes = None
	searchFilter = "cn=*"
	#cn[0]
	#print ldap.SCORE_SUBTREE
	print baseDN
	print searchFilter

	try:
		ldap_result_id = ldapo.search(baseDN, searchScope, searchFilter, retrieveAttributes)
		result_set = []
		while 1:
			result_type, result_data = ldapo.result(ldap_result_id, 0)
			if (result_data == []):
				break
			else:
				if result_type == ldap.RES_SEARCH_ENTRY:
					result_set.append(result_data)

		print result_set[0][0][1]['cn'][0]
		str_uid = result_set[0][0][1]['uid'][0]
		print result_set[0][0][1]['uidNumber'][0]
		print result_set[0][0][1]['gidNumber'][0]
		print result_set[0][0][1]['unixHomeDirectory'][0]
		print result_set[0][0][1]['loginShell'][0]
		
		# cat /etc/passwd | grep ^root: | sed -e 's/:.*//g'
		
		print "Check localuser '%s':" % str_uid
		#print pwd.getpwnam(str_uid)
		
		if not finduser(str_uid):
			print "    user not exists.... create"
			
			values = {
				"username": result_set[0][0][1]['uid'][0],
				"shell": result_set[0][0][1]['loginShell'][0],
				"uid": result_set[0][0][1]['uidNumber'][0],
				"gid": result_set[0][0][1]['gidNumber'][0],
				"homedir": result_set[0][0][1]['unixHomeDirectory'][0]
			}
			
			os.system("useradd -b /home/GM -d %(homedir)s -g %(gid)s -u %(uid)s %(username)s" % values)
		else:
			print "    user already exists."
	except ldap.LDAPError, e:
		print e

try:
	ldapo = ldap.initialize('ldap://172.16.2.201')
	ldapo.protocol_version = ldap.VERSION3
except ldap.LDAPError, e:
	print e
	sys.exit(2)

ldapo.simple_bind_s('cn=ldap,cn=users,dc=gm,dc=local', 'ldap')

"""
lc = ldapom.LdapConnection(uri='ldap://172.16.2.201', base='CN=ldap_test,CN=Users,DC=gm,DC=local', login='cn=ldap,cn=users,dc=gm,dc=local', password='ldap') 
"""

baseDN = "cn=users,dc=gm,dc=local"
searchScope = ldap.SCOPE_SUBTREE
## retrieve all attributes - again adjust to your needs - see documentation for more options
retrieveAttributes = None 
searchFilter = "cn=ldap_test"

try:
	ldap_result_id = ldapo.search(baseDN, searchScope, searchFilter, retrieveAttributes)
	result_set = []
	while 1:
		result_type, result_data = ldapo.result(ldap_result_id, 0)
		if (result_data == []):
			break
		else:
			if result_type == ldap.RES_SEARCH_ENTRY:
				result_set.append(result_data)

	for member in result_set[0][0][1]['member']:
		print member
		search_member_in_ldap(ldap, ldapo, member)

	#print "Group: %s" % result_set[0][0][0]
	#print "Members: %s" % result_set[0][0][1]['member']
	#search_member_in_ldap(ldap, ldapo, result_set[0][0][1]['member'])
except ldap.LDAPError, e:
	print e

