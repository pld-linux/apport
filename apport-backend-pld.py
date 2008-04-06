'''A concrete apport.PackageInfo class implementation for PLD.

Copyright (C) 2007 PLD Linux team
Author: Patryk Zawadzki <patrys@pld-linux.org>

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
the full text of the license.
'''

from packaging_rpm import RPMPackageInfo
from rpmUtils.miscutils import compareEVR, stringToVersion

class __PLDPackageInfo(RPMPackageInfo):
    '''Concrete apport.PackageInfo class implementation for PLD Linux.'''

    # A list of ids of official keys used by the project
    official_keylist = ('e64e7bf7')

    def is_distro_package(self, package):
        '''Check if a package is a genuine distro package (True) or comes from
        a third-party source.'''
        if RPMPackageInfo.is_distro_package(self,package):
            return True
        else:
            # GPG key check failed.
            hdr = RPMPackageInfo._get_header(self,package)

            if hdr['vendor'] == "PLD" and \
               hdr['distribution'].startswith("PLD"):
                return True
        return False

    def get_available_version(self, package):
        '''Return the latest available version of a package.'''
        # used in report.py, which is used by the frontends
        (epoch, name, ver, rel, arch) = self._split_envra(package)
        package_ver = '%s-%s' % (ver,rel)
        if epoch: 
            package_ver = "%s:%s" % (epoch, package_ver)
        # FIXME STUB
        return package_ver

    def get_source_tree(self, srcpackage, dir, version=None):
        '''Download given source package and unpack it into dir (which should
        be empty).

        This also has to care about applying patches etc., so that dir will
        eventually contain the actually compiled source.

        If version is given, this particular version will be retrieved.
        Otherwise this will fetch the latest available version.

        Return the directory that contains the actual source root directory
        (which might be a subdirectory of dir). Return None if the source is
        not available.'''
        # Used only by apport-retrace.
        # FIXME STUB
        return None

    def compare_versions(self, ver1, ver2):
        '''Compare two package versions.

        Return -1 for ver < ver2, 0 for ver1 == ver2, and 1 for ver1 > ver2.'''
        # Used by crashdb.py (i.e. the frontends)
        return compareEVR(stringToVersion(ver1),stringToVersion(ver2)) 

impl = __PLDPackageInfo()
