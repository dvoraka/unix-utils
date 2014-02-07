# -*- coding: utf-8 -*-
#

import subprocess
import pwd
import grp
import os
import time


'''Module for accessing Unix-like systems.'''


class Utils:

    def __init__(self):

        pass

    def user_exists(self, name):
        '''Check if user exists.'''
        
        try:

            pwd.getpwnam(name)

        except KeyError as err:

            return False

        return True

    def group_exists(self, name):
        '''Check if group exists.'''

        try:

            grp.getgrnam(name)

        except KeyError as err:

            return False

        return True

    def groups(self, username):
        
        groups = []
        for group in grp.getgrall():

            if username in group.gr_mem:

                groups.append(group.gr_name)

        return groups

    def user_group(self, username):
        
        user = pwd.getpwnam(username)
        gid = user.pw_gid
        group = grp.getgrgid(gid)

        return group.gr_name

    def all_groups(self, username):
        
        if not self.user_exists(username):

            return None

        grps = []

        grps.append(self.user_group(username))
        grps.extend(self.groups(username))

        return grps

    def add_user(
            self, login='', uid=-1,
            group='', home='', comment='',
            shell='', skel=''):
        '''Add user to system.'''

        command = (
            'useradd',
            '-u', str(uid),
            '-g', group,
            '-d', home,
            '-c', comment,
            '-s', shell,
            '-m', '-k', skel,
            login
        )

        print(command)

        try:

            return_code = subprocess.call(command)

        except OSError as error:

            print('add_user: Error({0}): {1}'.format(
                error.errno, error.strerror))
            self.log_message('add_user', error)

            return False

        if (return_code == 0):

            return True

        else:

            return False

    def add_group(self, name='', gid=-1):
        '''Add group to system.'''

        command = (
            'groupadd',
            '-g', str(gid),
            name
        )

        print(command)

        try:

            return_code = subprocess.call(command)

        except OSError as error:

            print('add_group: Error({0}): {1}'.format(
                error.errno, error.strerror))
            self.log_message('add_group', error)

            return False

        if(return_code == 0):

            return True

        else:

            return False

    def add_user_to_group(self, username, groupname):
        '''Add user to group.'''

        if not self.user_exists(username):

            return False

        command = (
            'usermod',
            '-a', '-G',
            groupname,
            username,
        )

        print(command)

        try:

            return_code = subprocess.call(command)

        except OSError as error:

            print('add_user_to_group: Error({0}): {1}'.format(
                error.errno, error.strerror))
            self.log_message('add_user_to_group', error)

            return False

        if (return_code == 0):

            return True

        else:

            return False

    def add_user_to_groups(self, username, groupnames):
        
        if ((not self.user_exists(username))
                or (groupnames is None)):

            print('Nonexistent user or groups')

            return
        
        for groupname in groupnames:

            self.add_user_to_group(username, groupname)

    def copy_groups(self, old_login, new_login):
        
        groups = self.all_groups(old_login)
        self.add_user_to_groups(new_login, groups)

    def add_samba_user(self, username, password):
        '''Add Samba user.'''
        
        command = (
            'smbpasswd',
            '-a', '-s',
            username
        )

        print(command)
        # depends on implementation
        password = password.decode('hex')

        proc = subprocess.Popen(command, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        pass_str = '{0}\n{1}\n'.format(password, password)
        ret_data = proc.communicate(pass_str)
        
        if (ret_data[1] != ''):

            print(ret_data[1])

        if (proc.returncode == 0):

            return True

        else:

            return False

    def samba_user_info(self, username):
        '''Return Samba user info.'''
        
        command = (
            'pdbedit',
            '-v',
            username
        )

        print(command)

        proc = subprocess.Popen(command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False)
        result = proc.communicate()
        
        if (proc.returncode == 0):

            return result[0]

        else:

            return None

    def disable_samba_user(self, username):

        command = (
            'smbpasswd',
            '-d',
            username,
        )

        print(command)

        try:

            return_code = subprocess.call(command)

        except OSError as error:

            print('disable_samba_user: Error({0}): {1}'.format(
                error.errno, error.strerror))
            self.log_message('disable_samba_user', error)

            return False

        if (return_code == 0):

            return True

        else:

            return False

    def enable_samba_user(self, username):

        command = (
            'smbpasswd',
            '-e',
            username,
        )

        print(command)

        try:

            return_code = subprocess.call(command)

        except OSError as error:

            print('enable_samba_user: Error({0}): {1}'.format(
                error.errno, error.strerror))
            self.log_message('enable_samba_user', error)

            return False

        if (return_code == 0):

            return True

        else:

            return False

    def set_quota(self, username, quota_name):
        '''Set quota.'''
        
        command = (
            'edquota',
            '-p',
            quota_name,
            username
        )

        print(command)

        try:

            return_code = subprocess.call(command)

        except OSError as error:

            print('set_quota: Error({0}): {1}'.format(
                error.errno, error.strerror))
            return False

        if (return_code == 0):

            return True

        else:

            return False

    def chmod(self, filename, mode):
        '''Set file mode.'''

        try:

            os.chmod(filename, mode)

        except OSError as error:

            self.log_message('chmod', error)
            return False

        return True

    def log_message(self, name, error):
        '''Create message and send it to logger().'''

        self.logger('{0}(): Error({1}): {2}'.format(
            name, error.errno, error.strerror))

        return 0
       
    def logger(self, message, filename='default.log'):
        '''Log message to file.'''

        with open(filename, 'a') as fileo:

            fmess = '{0} {1}\n'.format(time.asctime(), message)
            fileo.write(fmess)

        return 0
        
    def run_process():
        pass
