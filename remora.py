from botocore.exceptions import NoCredentialsError
from botocore.compat import OrderedDict
from botocore import xform_name

import botocore
from botocore.hooks import HierarchicalEmitter
from awscli.clidriver import ServiceCommand, CLIOperationCaller, \
    CLIDriver, ServiceOperation
from awscli import EnvironmentVariables
from awscli.plugin import load_plugins


def cli(profile=None):
    driver = create_clieval(profile)
    return driver


def create_clieval(profile):
    emitter = HierarchicalEmitter()
    session = botocore.session.Session(EnvironmentVariables, emitter)
    session.profile = profile
    # _set_user_agent_for_session(session)
    load_plugins(session.full_config.get('plugins', {}),
                 event_hooks=emitter)
    driver = CLIEval(session=session)
    return driver


class REPLServiceCommand(ServiceCommand):

    def _create_command_table(self):
        command_table = OrderedDict()
        service_object = self._get_service_object()
        for operation_object in service_object.operations:
            cli_name = xform_name(operation_object.name, '-')
            command_table[cli_name] = ServiceOperation(
                name=cli_name,
                parent_name=self._name,
                operation_object=operation_object,
                operation_caller=EvalOperationCaller(self.session),
                service_object=service_object)
        self.session.emit('building-command-table.%s' % self._name,
                          command_table=command_table,
                          session=self.session,
                          command_object=self)
        self._add_lineage(command_table)
        return command_table


class EvalOperationCaller(CLIOperationCaller):

    def invoke(self, operation_object, parameters, parsed_globals):
        if not self._session.get_credentials():
            raise NoCredentialsError()
        endpoint = operation_object.service.get_endpoint(
            region_name=parsed_globals.region,
            endpoint_url=parsed_globals.endpoint_url,
            verify=parsed_globals.verify_ssl)
        if operation_object.can_paginate and parsed_globals.paginate:
            response_data = operation_object.paginate(endpoint, **parameters)
            response_data = response_data.build_full_result()
        else:
            http_response, response_data = operation_object.call(endpoint,
                                                                 **parameters)
        return response_data


class CLIEval(CLIDriver):

    def __call__(self, cmdline):
        return CLIDriver.main(self, cmdline.split())

    def _build_builtin_commands(self, session):
        commands = OrderedDict()
        services = session.get_available_services()
        for service_name in services:
            commands[service_name] = REPLServiceCommand(
                cli_name=service_name, session=self.session,
                service_name=service_name)
        return commands
