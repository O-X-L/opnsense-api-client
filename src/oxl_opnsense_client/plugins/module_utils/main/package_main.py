from time import sleep

from ..main.package import Package
from ..base.api import Session


def process(m, p: dict, r: dict) -> None:
    s = Session(m=m)

    # pulling stati of all packages
    package_stati = Package(m=m, session=s, name='').search_call()

    for pkg_name in p['name']:
        pkg = Package(m=m, name=pkg_name, session=s)
        pkg.package_stati = package_stati
        pkg.check()

        # execute action if needed
        if pkg.r['diff']['before']['installed'] and \
                p['action'] in ['reinstall', 'remove', 'lock', 'unlock']:
            pkg.change_state()

        elif not pkg.r['diff']['before']['installed'] and \
                p['action'] == 'install':
            pkg.install()

        if pkg.r['changed']:
            sleep(p['post_sleep'])  # time for the box to update package info
            r['changed'] = True

        r['diff']['before'][pkg_name] = pkg.r['diff']['before']
        r['diff']['after'][pkg_name] = pkg.r['diff']['after']

    s.close()
