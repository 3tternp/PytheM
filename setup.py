#!/usr/bin/env python3
# coding=UTF-8

# Copyright (c) 2016-2018 Angelo Moura
#
# This file is part of the program pythem
#
# pythem is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA


from setuptools import find_packages, setup

setup(
    name="pythem",
    version="0.6.0",
    description="pentest framework",
    author="Angelo Moura",
    author_email="m4n3dw0lf@gmail.com",
    url="https://github.com/3tternp/PytheM",
    keywords=["pythem", "pentest", "framework", "hacking"],
    python_requires=">=3.8",
    packages=find_packages(include=["core", "core.*", "modules", "modules.*"]),
    install_requires=[
        "requests>=2.10.0",
        "scapy>=2.3.2",
        "netaddr>=0.7.18",
        "paramiko>=2.0.1",
        "termcolor>=1.1.0",
        "psutil>=4.3.0",
        'NetfilterQueue>=0.8.1; platform_system=="Linux"',
    ],
    scripts=["pythem/pythem"],
)
