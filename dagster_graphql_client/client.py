from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from typing import List, Optional, Dict, Any
import dagster_graphql_client.queries as queries


# Reference: https://github.com/dagster-io/dagster/blob/master/python_modules/dagster-graphql/dagster_graphql/client/client.py
class DagsterGraphQLClient:
    def __init__(self, url, verify_ssl: bool = False, retries: int = 3):

        self.client = Client(
            transport=RequestsHTTPTransport(
                url=url, verify=verify_ssl, retries=retries
            ),
            fetch_schema_from_transport=True,
        )

    def _execute(self, query: str, variables: Optional[Dict[str, Any]] = None) -> dict:
        return self.client.execute(gql(query), variable_values=variables)

    def repositories(self):
        return self._execute(queries.RepositoriesQuery)

    def jobs(self, repository_location_name: str, repository_name: str) -> dict:
        variables = {
            "repositoryLocationName": repository_location_name,
            "repositoryName": repository_name,
        }
        return self._execute(queries.JobsQuery, variables)

    def job_metadata(
        self, repository_location_name: str, repository_name: str, pipeline_name: str
    ) -> dict:
        variables = {
            "pipelineName": pipeline_name,
            "repositoryName": repository_name,
            "repositoryLocationName": repository_location_name,
        }
        return self._execute(queries.JobMetadataQuery, variables)

    def job_overview_sidebar(
        self, repository_location_name: str, repository_name: str, pipeline_name: str
    ) -> dict:
        variables = {
            "pipelineSelector": {
                "repositoryName": repository_name,
                "repositoryLocationName": repository_location_name,
                "pipelineName": pipeline_name,
            }
        }
        return self._execute(queries.JobOverviewSidebarQuery, variables)

    def run_launch(
        self,
        repository_location_name: str,
        repository_name: str,
        job_name: str,
        run_config_data: dict,
    ) -> dict:
        variables = {
            "repositoryLocationName": repository_location_name,
            "repositoryName": repository_name,
            "jobName": job_name,
            "runConfigData": run_config_data,
        }
        return self._execute(queries.LaunchRunMutation, variables)

    def run_terminate(self, run_id: str) -> dict:
        variables = {"runId": run_id}
        return self._execute(queries.TerminateRun, variables)

    def run_status(self, run_id) -> dict:
        variables = {"runId": run_id}
        return self._execute(queries.RunStatus, variables)

    def run_delete(self, run_id: str) -> dict:
        variables = {"runId": run_id}
        return self._execute(queries.Delete, variables)

    def runs_root(
        self,
        pipeline_name: Optional[str] = None,
        run_ids: List[str] = [],
        statuses: List[str] = [],
        limit=20,
    ) -> dict:

        filter: dict[str, Any] = {}
        queued_filter: dict[str, Any] = {"statuses": ["QUEUED"]}
        in_progress_filter: dict[str, Any] = {
            "statuses": ["STARTED", "STARTING", "CANCELING"]
        }

        if pipeline_name:
            filter["pipelineName"] = pipeline_name
            queued_filter["pipelineName"] = pipeline_name
            in_progress_filter["pipelineName"] = pipeline_name
        if run_ids:
            filter["runIds"] = run_ids
            queued_filter["runIds"] = run_ids
            in_progress_filter["runIds"] = run_ids
        if statuses:
            filter["statuses"] = statuses

        variables = {
            "filter": filter,
            "queuedFilter": queued_filter,
            "inProgressFilter": in_progress_filter,
            "limit": limit,
        }
        return self._execute(queries.RunsRootQuery, variables)

    def asset_wipe(self, asset_keys: List[str]) -> dict:
        variables = {
            "assetKeys": [
                {
                    "path": asset_keys,
                }
            ]
        }
        return self._execute(queries.AssetWipeMutation, variables)

    def asset_materializations(self, asset_keys: List[str], limit: int = 200) -> dict:
        variables = {"assetKey": {"path": asset_keys}, "limit": limit}
        return self._execute(queries.AssetMaterializationsQuery, variables)

    def permissions(self) -> dict:
        return self._execute(queries.PermissionsQuery)

    def root_workspace(self) -> dict:
        return self._execute(queries.RootWorkspaceQuery)

    def pipeline_explorer_root(
        self,
        repository_location_name: str,
        repository_name: str,
        pipeline_name: str,
        root_handle_id: str = "",
        request_scope_handle_id: str = "",
    ) -> dict:
        variables = {
            "snapshotPipelineSelector": {
                "repositoryName": repository_name,
                "repositoryLocationName": repository_location_name,
                "pipelineName": pipeline_name,
            },
            "rootHandleID": root_handle_id,
            "requestScopeHandleID": request_scope_handle_id,
        }
        return self._execute(queries.PipelineExplorerRootQuery, variables)

    def launchpad_root(
        self, repository_location_name: str, repository_name: str, pipeline_name: str
    ) -> dict:
        variables = {
            "repositoryName": repository_name,
            "repositoryLocationName": repository_location_name,
            "pipelineName": pipeline_name,
        }
        return self._execute(queries.LaunchpadRootQuery, variables)

    def pipeline_execution_config_schema(
        self,
        repository_location_name: str,
        repository_name: str,
        pipeline_name: str,
        mode: None,
    ) -> dict:
        variables = {
            "selector": {
                "repositoryName": repository_name,
                "repositoryLocationName": repository_location_name,
                "pipelineName": pipeline_name,
            },
            "mode": mode,
        }
        return self._execute(queries.PipelineExecutionConfigSchemaQuery, variables)

    def op_selector(
        self, repository_location_name: str, repository_name: str, pipeline_name: str
    ) -> dict:
        variables = {
            "pipelineName": pipeline_name,
            "repositoryLocationName": repository_location_name,
            "repositoryName": repository_name,
        }
        return self._execute(queries.OpSelectorQuery, variables)

    def launch_pipeline_execution(
        self,
        repository_location_name: str,
        repository_name: str,
        pipeline_name: str,
        execution_rcd: dict,
        ops_rcd: dict,
        resources_rcd: dict,
        mode="default",
        tags=[{"key": "dagster/solid_selection", "value": "*"}],
    ) -> dict:
        variables = {
            "executionParams": {
                "runConfigData": {
                    "execution": execution_rcd,
                    "ops": ops_rcd,
                    "resources": resources_rcd,
                },
                "selector": {
                    "repositoryName": repository_name,
                    "repositoryLocationName": repository_location_name,
                    "pipelineName": pipeline_name,
                },
                "mode": mode,
                "executionMetadata": {"tags": tags},
            }
        }
        return self._execute(queries.LaunchPipelineExecution, variables)

    def instance_schedules(self) -> dict:
        return self._execute(queries.InstanceSchedulesQuery)

    def instance_sensors(self) -> dict:
        return self._execute(queries.InstanceSensorsQuery)

    def sensor_stop(self, job_origin_id: str) -> dict:
        variables = {"jobOriginId": job_origin_id}
        return self._execute(queries.StopSensor, variables)

    def sensor_start(
        self, repository_location_name: str, repository_name: str, sensor_name: str
    ) -> dict:
        variables = {
            "sensorSelector": {
                "repositoryName": repository_name,
                "repositoryLocationName": repository_location_name,
                "sensorName": sensor_name,
            }
        }
        return self._execute(queries.StartSensor, variables)

    def instance_health(self) -> dict:
        return self._execute(queries.InstanceHealthQuery)

    def instance_config(self) -> dict:
        return self._execute(queries.InstanceConfigQuery)

    def reload_repository_location(self, repository_location_name: str) -> dict:
        variables = {"location": repository_location_name}
        return self._execute(queries.ReloadRepositoryLocationMutation, variables)
