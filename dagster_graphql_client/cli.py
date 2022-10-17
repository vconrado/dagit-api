import click
from datetime import datetime
from dagster_graphql_client import DagsterGraphQLClient
import yaml
import json
from mergedeep import merge

DATETIME_FMT='%Y-%m-%d %H:%M:%S'

@click.group()
@click.option('-t', '--protocol', required=False, help='Protocol (default=http)', default="http")
@click.option('-h', '--host', required=False, help='Dagit Host (default=0.0.0.0)', default="0.0.0.0")
@click.option('-p', '--port', required=False, help='Dagit Port (default=9003)', default="9003")
@click.option('-l', '--repository_location_name', required=False, help='repositoryLocationName (default=repository.py)', default="repository.py")
@click.option('-n', '--repository_name', required=False, help='repositoryName (default=repo)', default="repo")
@click.pass_context
def cli(ctx, protocol, host, port, repository_location_name, repository_name):
    """
    Dagit Client
    """
    ctx.obj = {
        'api': DagsterGraphQLClient(url=f"{protocol}://{host}:{port}/graphql"),
        'params': {
            'protocol': protocol,
            'host': host,
            'port': port   
        },
        'variables':
            {
                'repositoryLocationName': repository_location_name,
                'repositoryName':repository_name
            }
    }


def safe_gets(data, paths):
    result = data
    for p in paths:
        result = result.get(p, {})
    return result

@cli.group('instance')
@click.pass_context
def instance(ctx):
    pass

@instance.command('health')
@click.pass_context
def instance_health(ctx):
    api: DagitAPI = ctx.obj['api']
    print("# id, status")
    for daemon in safe_gets(api.InstanceHealthQuery(), ["instance", "daemonHealth", "allDaemonStatuses"]):
        print(f"{daemon['id']:9}:\t{'' if daemon['healthy'] else 'not'} running")
    


@cli.group('jobs')
@click.pass_context
def jobs(ctx):
    pass

@jobs.command('list')
@click.pass_context
def jobs_list(ctx):
    api: DagitAPI = ctx.obj['api']
    variables: dict = ctx.obj['variables']
    print("# name")
    for job in safe_gets(api.JobsQuery(**variables), ["repositoryOrError", "jobs"]):
        print(f"{job['name']}")



@cli.group('runs')
@click.pass_context
def runs(ctx):
    pass


@runs.command('list')
@click.option('--pipeline_name', required=False, help='pipelineName', default=None)
@click.option('--run_ids', required=False, help='runIds', multiple=True, default=[])
@click.option('--statuses', required=False, help='statuses', multiple=True, default=[])
@click.pass_context
def runs_list(ctx, pipeline_name, run_ids, statuses):
    api: DagitAPI = ctx.obj['api']
    variables = {}
    if pipeline_name:
        variables['pipelineName']=pipeline_name
    if run_ids:
        variables['runIds']=run_ids
    if statuses:
        variables['statuses']=statuses

    runs = api.RunsRootQuery(**variables)
    print("# pipelineName, id, startTime, endTime, status")
    for run in safe_gets(runs, ["pipelineRunsOrError", "results"]):
        print(f"{run['pipelineName']}, {run['id']}, {datetime.fromtimestamp(run['startTime']).strftime(DATETIME_FMT)}, {datetime.fromtimestamp(run['endTime']).strftime(DATETIME_FMT) if run['endTime'] else ''}, {run['status']}")


@runs.command('stop')
@click.argument('run_id', required=True)
@click.pass_context
def runs_stop(ctx, run_id):
    api: DagsterGraphQLClient = ctx.obj['api']
    result = api.TerminateRun(runId=run_id)
    type = safe_gets(result, ['terminateRun', '__typename'])
    if type == 'TerminateRunSuccess':
        print("Success")
    else:
        message = safe_gets(result, ['terminateRun', 'message'])
        print(f"Failure: {message}")

@runs.command('preset')
@click.argument('pipeline_name', required=True)
@click.argument('idx', required=True)
@click.argument('run_config', required=False)
@click.pass_context
def runs_preset(ctx, pipeline_name, idx, run_config):
    idx = int(idx)
    api: DagitAPI = ctx.obj['api']
    variables: dict = ctx.obj['variables']
    default_values = api.LaunchpadRootQuery(pipelineName=pipeline_name, 
            repositoryLocationName=variables['repositoryLocationName'],repositoryName=variables['repositoryName'])
    presets = safe_gets(default_values, ['pipelineOrError', 'presets'])
    if idx > len(presets) or idx < 0:
        raise Exception(f"Invalid preset index '{idx}'. Max: {len(presets)}")
    preset = presets[idx]
    runConfig = yaml.safe_load(preset['runConfigYaml'])
    if run_config:
        run_config_json = json.loads(run_config)
        runConfig = merge({}, runConfig, run_config_json)
    result = api.LaunchRunMutation(
        jobName=pipeline_name,
        repositoryLocationName=variables['repositoryLocationName'],repositoryName=variables['repositoryName'],
        runConfigData=runConfig
    )
    if safe_gets(result, ['launchRun', '__typename']) == 'LaunchRunSuccess':
        print(safe_gets(result, ['launchRun', 'run', 'runId']))
    else:
        message = safe_gets(result, ['launchRun', 'message'])
        print(f"Failure: {message}")


if __name__ == '__main__':
    # cli(sys.argv[1:])
    # cli(["instance", "health"])
    # cli(["jobs", "list"])
    # cli(["runs", "list"])
    # cli(["runs", "list", "--run_ids", "387162ff-be2c-4240-821a-60cebcdad9d7", "cbb46481-08e0-4a2f-9794-84a516be638d"])
    # cli(["runs", "stop", "f55471f0-21f2-4085-ae15-75e6750f7b61"])
    cli(["runs", "preset", "110_lc8_curuai_ddi_by_feature", "0", '{"ops":{"discovery_external_by_feature":{"config":{"limit":2, "offset":0}}}}'])

