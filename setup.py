#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-old-world-radio.jarbasai=skill_old_world_radio:OldWorldRadioSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-old-world-radio',
    version='0.0.1',
    description='ovos old world radio skill plugin',
    url='https://github.com/JarbasSkills/skill-old-world-radio',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_old_world_radio": ""},
    package_data={'skill_old_world_radio': ['locale/*', 'ui/*', 'res/*']},
    packages=['skill_old_world_radio'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
