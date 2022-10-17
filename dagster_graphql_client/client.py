from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from typing import List, Optional, Dict, Any
import dagster_graphql_client.queries as queries


# Reference: https://github.com/dagster-io/dagster/blob/master/python_modules/dagster-graphql/dagster_graphql/client/client.py
class DagsterGraphQLClient:
    def __init__(
            self, 
            url, 
            verify_ssl:Optional[bool]=False, 
            retries:Optional[int]=3):
        self.client = Client(transport=RequestsHTTPTransport(url=url, verify=verify_ssl, retries=retries), 
                                fetch_schema_from_transport=True)

    def _execute(self, query: str, variables:Optional[Dict[str, Any]] = None) -> dict:
        return self.client.execute(gql(query), variable_values=variables)
   
    def RepositoriesQuery(self):
    
        return self._execute(queries.RepositoriesQuery)
    
    def JobsQuery(self, repositoryLocationName: str, repositoryName: str) -> dict:
        variables = {
                        "repositoryLocationName": repositoryLocationName,
                        "repositoryName": repositoryName
                    }
        return self._execute(queries.JobsQuery, variables)

    def LaunchRunMutation(self, repositoryLocationName: str, repositoryName: str, 
                            jobName: str, runConfigData: str) -> dict:
        variables = {
                        "repositoryLocationName": repositoryLocationName,
                        "repositoryName": repositoryName,
                        "jobName": jobName,
                        "runConfigData": runConfigData
                    }

        return self._execute(queries.LaunchRunMutation, variables)

    def TerminateRun(self, runId: str) -> dict:
        variables = {"runId": runId}

        return self._execute(queries.TerminateRun, variables)

    def RunStatus(self, runId) -> dict:
        variables = {"runId": runId}

        return self._execute(queries.RunStatus, variables)

    def AssetWipeMutation(self, assetKeys: str) -> dict:
        variables = {"assetKeys": [{"path": [assetKeys, ]}]}

        return self._execute(queries.AssetWipeMutation, variables)

    def AssetMaterializationsQuery(self, assetKeys: List[str], limit: int = 200) -> dict:

        variables = {"assetKey": {"path": assetKeys}, "limit": limit}

        return self._execute(queries.AssetMaterializationsQuery, variables)

    def PermissionsQuery(self) -> dict:
        return self._execute(queries.PermissionsQuery)

    def RootWorkspaceQuery(self) -> dict:
        return self._execute(queries.RootWorkspaceQuery)

    def JobMetadataQuery(self, repositoryLocationName: str, repositoryName:str, pipelineName: str) -> dict:
        variables={
            "pipelineName": pipelineName,
            "repositoryName": repositoryName,
            "repositoryLocationName": repositoryLocationName
            }
        return self._execute(queries.JobMetadataQuery, variables)

    def PipelineExplorerRootQuery(self, repositoryLocationName: str, repositoryName:str, pipelineName: str,
                                    rootHandleID: str="", requestScopeHandleID: str="") -> dict:
        variables={
                    "snapshotPipelineSelector": 
                    {
                        "repositoryName": repositoryName,
                        "repositoryLocationName": repositoryLocationName,
                        "pipelineName": pipelineName
                    },
                    "rootHandleID": rootHandleID,
                    "requestScopeHandleID": requestScopeHandleID
                }
        return self._execute(queries.PipelineExplorerRootQuery, variables)

    def JobOverviewSidebarQuery(self, repositoryLocationName: str, repositoryName:str, pipelineName: str) -> dict:
        variables={
            "pipelineSelector": {
                "repositoryName": repositoryName,
                "repositoryLocationName": repositoryLocationName,
                "pipelineName": pipelineName
            }
        }
        return self._execute(queries.JobOverviewSidebarQuery, variables)

    def LaunchpadRootQuery(self, repositoryLocationName: str, repositoryName:str, pipelineName: str) -> dict:
        variables={
            "repositoryName": repositoryName,
            "repositoryLocationName": repositoryLocationName,
            "pipelineName": pipelineName
        }
        return self._execute(queries.LaunchpadRootQuery, variables)
    
    def PipelineExecutionConfigSchemaQuery(self, repositoryLocationName: str, repositoryName:str, pipelineName: str, mode: None) -> dict:
        variables={
            "selector": {
                "repositoryName": repositoryName,
                "repositoryLocationName": repositoryLocationName,
                "pipelineName": pipelineName
            },
            "mode": mode
        }
        return self._execute(queries.PipelineExecutionConfigSchemaQuery, variables)
    
    def OpSelectorQuery(self, repositoryLocationName: str, repositoryName:str, pipelineName: str) -> dict:
        variables = {
            'pipelineName': pipelineName,
            'repositoryLocationName': repositoryLocationName,
            'repositoryName': repositoryName
        }
        return self._execute(queries.OpSelectorQuery, variables)

    def LaunchPipelineExecution(self, repositoryLocationName: str, repositoryName:str, pipelineName: str,
        execution_rcd: dict, ops_rcd:dict, resources_rcd:dict, mode="default", tags=[{"key": "dagster/solid_selection","value": "*"}]) -> dict:
        variables={
                "executionParams": {
                    "runConfigData": {
                        "execution": execution_rcd,
                        "ops": ops_rcd,
                        "resources": resources_rcd
                    },
                    "selector": {
                        "repositoryName": repositoryName,
                        "repositoryLocationName": repositoryLocationName,
                        "pipelineName": pipelineName
                    },
                    "mode": mode,
                    "executionMetadata": {
                    "tags": tags
                    }
                }
            }
        return self._execute(queries.LaunchPipelineExecution, variables)


    def RunsRootQuery(self, pipelineName:str=None, runIds: List[str]=[], statuses:List[str]=[], limit=20) -> dict:
        
        filter={}
        queuedFilter={
            "statuses": [
                "QUEUED"
            ]
        }
        inProgressFilter={
            "statuses": [
                "STARTED",
                "STARTING",
                "CANCELING"
            ]
        }

        if pipelineName:
            filter["pipelineName"] = pipelineName
            queuedFilter["pipelineName"] = pipelineName
            inProgressFilter["pipelineName"] = pipelineName
        if runIds:
            filter["runIds"] = runIds
            queuedFilter["runIds"] = runIds
            inProgressFilter["runIds"] = runIds
        if statuses:
            filter["statuses"] = statuses
        
        variables = {
                        "filter": filter,
                        "queuedFilter": queuedFilter,
                        "inProgressFilter": {
                                "pipelineName": pipelineName,
                                "runIds": runIds,
                                "statuses": [
                                    "STARTED",
                                    "STARTING",
                                    "CANCELING"
                                ]
                            },
                            "limit": limit
                    }
        return self._execute(queries.RunsRootQuery, variables)

    def InstanceSchedulesQuery(self) -> dict:
        return self._execute(queries.InstanceSchedulesQuery)

    def InstanceSensorsQuery(self) -> dict:
        return self._execute(queries.InstanceSensorsQuery)

    def StopSensor(self, jobOriginId:str) -> dict:
        variables={
            "jobOriginId": jobOriginId
        }
        return self._execute(queries.StopSensor, variables)

    def StartSensor(self, repositoryLocationName: str, repositoryName:str, sensorName:str) -> dict:
        variables={
            "sensorSelector": {
                "repositoryName": repositoryName,
                "repositoryLocationName": repositoryLocationName,
                "sensorName": sensorName
            }
        }
        return self._execute(queries.StartSensor, variables)
    
    def InstanceHealthQuery(self) -> dict:
        return self._execute(queries.InstanceHealthQuery)

    def InstanceConfigQuery(self) -> dict:
        return self._execute(queries.InstanceConfigQuery)

    def ReloadRepositoryLocationMutation(self, repositoryLocationName:str) -> dict:
        variables={"location": repositoryLocationName}
        return self._execute(queries.ReloadRepositoryLocationMutation, variables)
    
    def Delete(self, runId:str) -> dict:
        variables={"runId": runId}
        return self._execute(queries.Delete, variables)

    