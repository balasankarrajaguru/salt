# -*- coding: utf-8 -*-
'''
State modules to interact with Junos devices.
==============================================

:maturity: new
:dependencies: junos-eznc, jxmlease

.. note::

    Those who wish to use junos-eznc (PyEZ) version >= 2.1.0, must
    use the latest salt code from github until the next release.

Refer to :mod:`junos <salt.proxy.junos>` for information on connecting to junos proxy.
'''
from __future__ import absolute_import

import logging

log = logging.getLogger()


def rpc(name, dest=None, format='xml', args=None, **kwargs):
    '''
    Executes the given rpc. The returned data can be stored in a file
    by specifying the destination path with dest as an argument

    .. code-block:: yaml

        get-interface-information:
            junos:
              - rpc
              - dest: /home/user/rpc.log
              - interface_name: lo0


    Parameters:
      Required
        * cmd:
          The rpc to be executed. (default = None)
      Optional
        * dest:
          Destination file where the rpc ouput is stored. (default = None)
          Note that the file will be stored on the proxy minion. To push the
          files to the master use the salt's following execution module: \
            :py:func:`cp.push <salt.modules.cp.push>`
        * format:
          The format in which the rpc reply must be stored in file specified in the dest
          (used only when dest is specified) (default = xml)
        * kwargs: keyworded arguments taken by rpc call like-
            * timeout:
              Set NETCONF RPC timeout. Can be used for commands which
              take a while to execute. (default= 30 seconds)
            * filter:
              Only to be used with 'get-config' rpc to get specific configuration.
            * terse:
              Amount of information you want.
            * interface_name:
              Name of the interface whose information you want.
    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    if args is not None:
        ret['changes'] = __salt__['junos.rpc'](
            name,
            dest,
            format,
            *args,
            **kwargs)
    else:
        ret['changes'] = __salt__['junos.rpc'](name, dest, format, **kwargs)
    return ret


def set_hostname(name, **kwargs):
    '''
    Changes the hostname of the device.

    .. code-block:: yaml

            device_name:
              junos:
                - set_hostname
                - comment: "Host-name set via saltstack."


    Parameters:
     Required
        * hostname: The name to be set. (default = None)
     Optional
        * kwargs: Keyworded arguments which can be provided like-
            * timeout:
              Set NETCONF RPC timeout. Can be used for commands
              which take a while to execute. (default = 30 seconds)
            * comment:
              Provide a comment to the commit. (default = None)
            * confirm:
              Provide time in minutes for commit confirmation. \
              If this option is specified, the commit will be rollbacked in \
              the given time unless the commit is confirmed.

    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.set_hostname'](name, **kwargs)
    return ret


def commit(name, **kwargs):
    '''
    Commits the changes loaded into the candidate configuration.

    .. code-block:: yaml

            commit the changes:
              junos:
                - commit
                - confirm: 10


    Parameters:
      Optional
        * kwargs: Keyworded arguments which can be provided like-
            * timeout:
              Set NETCONF RPC timeout. Can be used for commands which take a \
              while to execute. (default = 30 seconds)
            * comment:
              Provide a comment to the commit. (default = None)
            * confirm:
              Provide time in minutes for commit confirmation. If this option \
              is specified, the commit will be rollbacked in the given time \
              unless the commit is confirmed.
            * sync:
              On dual control plane systems, requests that the candidate\
              configuration on one control plane be copied to the other \
              control plane,checked for correct syntax, and committed on \
              both Routing Engines. (default = False)
            * force_sync:
              On dual control plane systems, force the candidate configuration
              on one control plane to be copied to the other control plane.
            * full:
              When set to True requires all the daemons to check and evaluate \
              the new configuration.
            * detail:
              When true return commit detail.
    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.commit'](**kwargs)
    return ret


def rollback(name, id, **kwargs):
    '''
    Rollbacks the committed changes.

    .. code-block:: yaml

            rollback the changes:
              junos:
                - rollback
                - id: 5

    Parameters:
      Optional
        * id:
          The rollback id value [0-49]. (default = 0)
        * kwargs: Keyworded arguments which can be provided like-
            * timeout:
              Set NETCONF RPC timeout. Can be used for commands which
              take a while to execute. (default = 30 seconds)
            * comment:
              Provide a comment to the commit. (default = None)
            * confirm:
              Provide time in minutes for commit confirmation. If this option \
              is specified, the commit will be rollbacked in the given time \
              unless the commit is confirmed.
            * diffs_file:
              Path to the file where any diffs will be written. (default = None)

    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.rollback'](id, **kwargs)
    return ret


def diff(name, d_id):
    '''
    Gets the difference between the candidate and the current configuration.

    .. code-block:: yaml

            get the diff:
              junos:
                - diff
                - id: 10

    Parameters:
      Optional
        * id:
          The rollback id value [0-49]. (default = 0)
    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.diff'](d_id)
    return ret


def cli(name, format='text', **kwargs):
    '''
    Executes the CLI commands and reuturns the text output.

    .. code-block:: yaml

            show version:
              junos:
                - cli
                - format: xml

    Parameters:
      Required
        * command:
          The command that need to be executed on Junos CLI. (default = None)
      Optional
        * format:
          Format in which to get the CLI output. (text or xml, \
            default = 'text')
        * kwargs: Keyworded arguments which can be provided like-
            * timeout:
              Set NETCONF RPC timeout. Can be used for commands which
              take a while to execute. (default = 30 seconds)
            * dest:
              The destination file where the CLI output can be stored.\
               (default = None)
    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.cli'](name, format, **kwargs)
    return ret


def shutdown(name, **kwargs):
    '''
    Shuts down the device.

    .. code-block:: yaml

            shut the device:
              junos:
                - shutdown
                - in_min: 10

    Parameters:
      Optional
        * kwargs:
            * reboot:
              Whether to reboot instead of shutdown. (default=False)
            * at:
              Specify time for reboot. (To be used only if reboot=yes)
            * in_min:
              Specify delay in minutes for shutdown
    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.shutdown'](**kwargs)
    return ret


def install_config(name, **kwargs):
    '''
    Loads and commits the configuration provided.

    .. code-block:: yaml

            Install the mentioned config:
              junos:
                - install_config
                - path: salt//configs/interface.set
                - timeout: 100
                - diffs_file: 'var/log/diff'


    .. code-block:: yaml

            Install the mentioned config:
              junos:
                - install_config
                - template_path: salt//configs/interface.set
                - timeout: 100
                - template_vars:
                    interface_name: lo0
                    description: Creating interface via SaltStack.


    Parameters:
      Required
        * name:
          Path where the configuration/template file is present. If the file has a \
          '*.conf' extension,
          the content is treated as text format. If the file has a '*.xml' \
          extension,
          the content is treated as XML format. If the file has a '*.set' \
          extension,
          the content is treated as Junos OS 'set' commands.(default = None)
      Optional
        * kwargs: Keyworded arguments which can be provided like-
            * template_vars:
              The dictionary of data for the jinja variables present in the \
              jinja template
            * timeout:
              Set NETCONF RPC timeout. Can be used for commands which
              take a while to execute. (default = 30 seconds)
            * overwrite:
              Set to True if you want this file is to completely replace the\
               configuration file. (default = False)
            * replace:
              Specify whether the configuration file uses "replace:" statements.
              Those statements under the 'replace' tag will only be changed.\
               (default = False)
            * comment:
              Provide a comment to the commit. (default = None)
            * confirm:
              Provide time in minutes for commit confirmation.
              If this option is specified, the commit will be rollbacked in \
              the given time unless the commit is confirmed.
            * diffs_file:
              Path to the file where the diff (difference in old configuration
              and the commited configuration) will be stored.(default = None)
              Note that the file will be stored on the proxy minion. To push the
              files to the master use the salt's following execution module: \
              :py:func:`cp.push <salt.modules.cp.push>`
    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.install_config'](name, **kwargs)
    return ret


def zeroize(name):
    '''
    Resets the device to default factory settings.

    .. code-block:: yaml

            reset my device:
              junos.zeroize

    name: can be anything
    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.zeroize']()
    return ret


def install_os(name, **kwargs):
    '''
    Installs the given image on the device. After the installation is complete
    the device is rebooted, if reboot=True is given as a keyworded argument.

    .. code-block:: yaml

            salt://images/junos_image.tgz:
              junos:
                - install_os
                - timeout: 100
                - reboot: True

    Parameters:
      Required
        * path:
          Path where the image file is present on the pro\
          xy minion.
      Optional
        * kwargs: keyworded arguments to be given such as timeout, reboot etc
            * timeout:
              Set NETCONF RPC timeout. Can be used to RPCs which
              take a while to execute. (default = 30 seconds)
            * reboot:
              Whether to reboot after installation (default = False)
            * no_copy:
              When True the software package will not be SCP’d to the device. \
              (default = False)

    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.install_os'](name, **kwargs)
    return ret


def file_copy(name, dest=None, **kwargs):
    '''
    Copies the file from the local device to the junos device.

    .. code-block:: yaml

            /home/m2/info.txt:
              junos:
                - file_copy
                - dest: info_copy.txt

    Parameters:
      Required
        * src:
          The sorce path where the file is kept.
        * dest:
          The destination path where the file will be copied.
    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.file_copy'](name, dest, **kwargs)
    return ret


def lock(name):
    """
    Attempts an exclusive lock on the candidate configuration. This
    is a non-blocking call.

    .. note::
        Any user who wishes to use lock, must necessarily unlock the
        configuration too. Ensure :py:func:`unlock <salt.states.junos.unlock>`
        is called in the same orchestration run in which the lock is called.

    .. code-block:: yaml

            lock the config:
              junos.lock

    """
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.lock']()
    return ret


def unlock(name):
    """
    Unlocks the candidate configuration.

    .. code-block:: yaml

            unlock the config:
              junos.unlock

    """
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.unlock']()
    return ret


def load(name, **kwargs):
    """
    Loads the configuration provided onto the junos device.

    .. code-block:: yaml

            Install the mentioned config:
              junos:
                - load
                - path: salt//configs/interface.set

    .. code-block:: yaml

            Install the mentioned config:
              junos:
                - load
                - template_path: salt//configs/interface.set
                - template_vars:
                    interface_name: lo0
                    description: Creating interface via SaltStack.


    Parameters:
      Required
        * name:
          Path where the configuration/template file is present. If the file has a \
          '*.conf' extension,
          the content is treated as text format. If the file has a '*.xml' \
          extension,
          the content is treated as XML format. If the file has a '*.set' \
          extension,
          the content is treated as Junos OS 'set' commands.(default = None)
      Optional
        * kwargs: Keyworded arguments which can be provided like-
            * overwrite:
              Set to True if you want this file is to completely replace the\
              configuration file. (default = False)
            * replace:
              Specify whether the configuration file uses "replace:" statements.
              Those statements under the 'replace' tag will only be changed.\
               (default = False)
            * format:
              Determines the format of the contents.
            * update:
              Compare a complete loaded configuration against
              the candidate configuration. For each hierarchy level or
              configuration object that is different in the two configurations,
              the version in the loaded configuration replaces the version in the
              candidate configuration. When the configuration is later committed,
              only system processes that are affected by the changed configuration
              elements parse the new configuration. This action is supported from
              PyEZ 2.1 (default = False)
            * template_vars:
              Variables to be passed into the template processing engine in addition
              to those present in __pillar__, __opts__, __grains__, etc.
              You may reference these variables in your template like so:
              {{ template_vars["var_name"] }}

    """
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.load'](name, **kwargs)
    return ret


def commit_check(name):
    """

    Perform a commit check on the configuration.

    .. code-block:: yaml

        perform commit check:
          junos.commit_check

    """
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.commit_check']()
    return ret


def get_table(name, table, file, path=None):
    '''
    Retrieve data from a Junos device using Tables/Views

    .. code-block:: yaml

        get route details:
            junos:
              - get_table
              - table: RouteTable
              - file: routes.yml


    Parameters:
      Required
        * name:
          task definition
        * table:
          Name of PyEZ Table
        * file:
          YAML file that has the table specified in table parameter
      Optional
        * path:
          Path of location of the YAML file.
          defaults to op directory in jnpr.junos.op
    '''
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    ret['changes'] = __salt__['junos.get_table'](table, file, path)
    return ret