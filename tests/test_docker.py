
def test_hosts_file(File):
    hosts = File('/etc/hosts')
    assert hosts.user == 'root'
    assert hosts.group == 'root'


def test_zabbixagent_running_and_enabled(Service):
    zabbixagent = Service("zabbix-agent")
    assert zabbixagent.is_enabled
    assert zabbixagent.is_running


def test_zabbix_agent_dot_conf(File):
    passwd = File("/etc/zabbix/zabbix_agentd.conf")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644

    assert passwd.contains("Server=192.168.3.33")
    assert passwd.contains("ServerActive=192.168.3.33")
    assert passwd.contains("ListenIP=0.0.0.0")


def test_zabbix_include_dir(File):
    zabbixagent = File("/etc/zabbix/zabbix_agentd.d")
    assert zabbixagent.is_directory
    assert zabbixagent.user == "root"
    assert zabbixagent.group == "root"


def test_socker(Socket):
    assert Socket("tcp://0.0.0.0:10050").is_listening


def test_zabbix_package(Package, SystemInfo):
    zabbixagent = Package('zabbix-agent')
    assert zabbixagent.is_installed

    if SystemInfo.distribution == 'debian':
        assert zabbixagent.version.startswith("1:3.0")
    if SystemInfo.distribution == 'centos':
        assert zabbixagent.version.startswith("3.0")
