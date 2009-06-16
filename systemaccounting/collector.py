import platform
import subprocess

class UserAccountingItem(object):
    """UserAccountingItem object represents
       accounting info for one user and per one period of time

       In short one UserAccountingItem object represents one line from sa(1) utily
       (one object per one line, one object per user)
       
       OpenBSD example: /usr/bin/sa -mki /var/account/acct.0
    """
    def __init__(self, username, number_of_commands, cputime, io_operaions, cpu_integral):
        self.__item = {}
        # TODO: isinstance
        if not isinstance(username, str):
            raise ValueError("username should be a str()")
        
        self.__item = {'username': username,
            'number_of_commands': number_of_commands,
            'cputime': cputime,
            'io_operaions': io_operaions,
            'cpu_integral': cpu_integral,}

    def __str__(self):
        return str(self.__item)
    
    @property
    def getUsername(self):
        return self.__item.get('username')

    @property
    def getNumberOfCommands(self):
        return self.__item.get('number_of_commands')

    @property
    def getCputime(self):
        return self.__item.get('cputime')

    @property
    def getIOoperations(self):
        return self.__item.get('userio_operaionsname')
    
    @property
    def getCPUintegral(self):
        return self.__item.get('cpu_integral')
    

    

class AccoutingAbstract(object):
    OSVERSION = ""
    
    def __init__(self):
        if platform.system() != self.OSVERSION:
            raise OSError("Incorrect Accounting used. OSVersion = %s, %s excpected" % (platform.system(), self.OSVERSION))

    def grabDaily(self):
        """
        Imports accounting statistics for past day

        returns list() of AccountingItem() objects
        for past day

        """
        raise NotImplemented("method should be redefined in a subclass")
    
    def grabLive(self):
        """
        Imports accounting statistics from live system.
        Usefull for close to realtime accounting grabbing.

        returns list() of AccountingItem() objects.
        TODO: think how period of time will be represented
        """
        raise NotImplemented("method should be redefined in a subclass")


class AccountingOpenbsd(AccoutingAbstract):
    """
    Collector for OpenBSD OS.
    acct(5) system stores its data files in the /var/account/ directory.
    
    By default file /var/account/acct rotates each 24h by /etc/daily script (at 3 AM)
    /var/account/acct   -- current (live) file
    /var/account/acct.0 -- accounting info for past day
    /var/account/acct.1 -- acct info two days ago
    /var/account/acct.2 -- acct info three days ago
    """
    
    DAILY_FILE = "/var/account/acct.0"
    OSVERSION = "OpenBSD" # `uname -s`
            
    def grabDaily(self):
        # TODO: check if created date of DAILY_FILE is last day
        cmd = ['/usr/sbin/sa', '-mki', self.DAILY_FILE]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = p.communicate()
        exitcode = p.wait()
        print "exitcode", cmd
        if exitcode != 0:
            raise RuntimeError("%s exits with non zero status: %s" % (cmd, e))

        result = list()
        for row in o.splitlines():
            #root         29269        38.77cpu       996213tio           0k
            (username, number_of_commands, cputime, io_operaions, cpu_integral) = \
                row.split()
            accountingItem = UserAccountingItem(username, number_of_commands, cputime, io_operaions, cpu_integral)
            result.append(accountingItem)

        if len(result) > 0:
            return result
        else:
            return None


if __name__ == '__main__':
    for accountingItem in AccountingOpenbsd().grabDaily():
        print accountingItem
