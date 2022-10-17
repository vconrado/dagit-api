RepositoriesQuery="""
            query RepositoriesQuery {
                repositoriesOrError {
                    ... on RepositoryConnection {
                    nodes {
                        name
                        location {
                        name
                        }
                    }
                    }
                }
            }
        """


    
JobsQuery="""
    query JobsQuery(
        $repositoryLocationName: String!
        $repositoryName: String!
        ) {
        repositoryOrError(
            repositorySelector: {
            repositoryLocationName: $repositoryLocationName
            repositoryName: $repositoryName
            }
        ) {
            ... on Repository {
            jobs {
                name
            }
            }
        }
        }
"""

LaunchRunMutation="""
    mutation LaunchRunMutation(
        $repositoryLocationName: String!
        $repositoryName: String!
        $jobName: String!
        $runConfigData: RunConfigData!
        ) {
        launchRun(
            executionParams: {
            selector: {
                repositoryLocationName: $repositoryLocationName
                repositoryName: $repositoryName
                jobName: $jobName
            }
            runConfigData: $runConfigData
            }
        ) {
            __typename
            ... on LaunchRunSuccess {
            run {
                runId
            }
            }
            ... on RunConfigValidationInvalid {
            errors {
                message
                reason
            }
            }
            ... on PythonError {
            message
            }
        }
        }
    """


TerminateRun="""
    mutation TerminateRun($runId: String!) {
        terminateRun(runId: $runId){
            __typename
            ... on TerminateRunSuccess{
            run {
                runId
            }
            }
            ... on TerminateRunFailure {
            message
            }
            ... on RunNotFoundError {
            runId
            }
            ... on PythonError {
            message
            stack
            }
        }
        }
    """

RunStatus="""
    query RunStatus($runId: ID!) {
    pipelineRunOrError(runId: $runId) {
        __typename
        ... on PipelineRun {
            status
        }
        ... on PipelineRunNotFoundError {
        message
        }
        ... on PythonError {
        message
        }
    }
    }
"""

AssetWipeMutation = """
    mutation AssetWipeMutation($assetKeys: [AssetKeyInput!]!) {
        wipeAssets(assetKeys: $assetKeys) {
            ... on AssetWipeSuccess {
            assetKeys {
                path
                __typename
            }
            __typename
            }
            ... on PythonError {
            message
            stack
            __typename
            }
            __typename
        }
    }
"""

AssetMaterializationsQuery = """
    query AssetMaterializationsQuery(
        $assetKey: AssetKeyInput!, 
        $limit: Int!, 
        $before: String) {
        assetOrError(assetKey: $assetKey) {
            ... on Asset {
            id
            key {
                path
                __typename
            }
            assetMaterializations(limit: $limit, beforeTimestampMillis: $before) {
                ...AssetMaterializationFragment
                __typename
            }
            __typename
            }
            __typename
        }
        }

        fragment AssetMaterializationFragment on AssetMaterialization {
        partition
        runOrError {
            ... on PipelineRun {
            id
            runId
            mode
            repositoryOrigin {
                id
                repositoryName
                repositoryLocationName
                __typename
            }
            status
            pipelineName
            pipelineSnapshotId
            __typename
            }
            __typename
        }
        materializationEvent {
            runId
            timestamp
            stepKey
            stepStats {
            endTime
            startTime
            __typename
            }
            materialization {
            label
            description
            metadataEntries {
                ...MetadataEntryFragment
                __typename
            }
            __typename
            }
            assetLineage {
            ...AssetLineageFragment
            __typename
            }
            __typename
        }
        __typename
        }

        fragment MetadataEntryFragment on EventMetadataEntry {
        __typename
        label
        description
        ... on EventPathMetadataEntry {
            path
            __typename
        }
        ... on EventJsonMetadataEntry {
            jsonString
            __typename
        }
        ... on EventUrlMetadataEntry {
            url
            __typename
        }
        ... on EventTextMetadataEntry {
            text
            __typename
        }
        ... on EventMarkdownMetadataEntry {
            mdStr
            __typename
        }
        ... on EventPythonArtifactMetadataEntry {
            module
            name
            __typename
        }
        ... on EventFloatMetadataEntry {
            floatValue
            __typename
        }
        ... on EventIntMetadataEntry {
            intValue
            intRepr
            __typename
        }
        ... on EventPipelineRunMetadataEntry {
            runId
            __typename
        }
        ... on EventAssetMetadataEntry {
            assetKey {
            path
            __typename
            }
            __typename
        }
        }

        fragment AssetLineageFragment on AssetLineageInfo {
        assetKey {
            path
            __typename
        }
        partitions
        __typename
        }
"""

PermissionsQuery="""query PermissionsQuery {
  permissions {
    ...PermissionFragment
    __typename
  }
}

fragment PermissionFragment on GraphenePermission {
  permission
  value
  __typename
}"""


RootWorkspaceQuery="""query RootWorkspaceQuery {
  workspaceOrError {
    __typename
    ... on Workspace {
      locationEntries {
        __typename
        id
        name
        loadStatus
        displayMetadata {
          key
          value
          __typename
        }
        updatedTimestamp
        locationOrLoadError {
          ... on RepositoryLocation {
            id
            isReloadSupported
            serverId
            name
            repositories {
              id
              name
              pipelines {
                id
                name
                isJob
                graphName
                pipelineSnapshotId
                modes {
                  id
                  name
                  __typename
                }
                __typename
              }
              schedules {
                id
                mode
                name
                pipelineName
                scheduleState {
                  id
                  status
                  __typename
                }
                __typename
              }
              sensors {
                id
                name
                targets {
                  mode
                  pipelineName
                  __typename
                }
                sensorState {
                  id
                  status
                  __typename
                }
                __typename
              }
              partitionSets {
                id
                mode
                pipelineName
                __typename
              }
              ...RepositoryInfoFragment
              __typename
            }
            __typename
          }
          ... on PythonError {
            ...PythonErrorFragment
            __typename
          }
          __typename
        }
      }
      __typename
    }
    ...PythonErrorFragment
  }
}

fragment PythonErrorFragment on PythonError {
  __typename
  message
  stack
  cause {
    message
    stack
    __typename
  }
}

fragment RepositoryInfoFragment on Repository {
  id
  name
  location {
    id
    name
    __typename
  }
  displayMetadata {
    key
    value
    __typename
  }
  __typename
}"""


JobMetadataQuery="""query JobMetadataQuery($params: PipelineSelector!, $runsFilter: RunsFilter) {
  pipelineOrError(params: $params) {
    ... on Pipeline {
      id
      ...JobMetadataFragment
      __typename
    }
    __typename
  }
  pipelineRunsOrError(filter: $runsFilter, limit: 5) {
    ... on PipelineRuns {
      results {
        id
        ...RunMetadataFragment
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment JobMetadataFragment on Pipeline {
  id
  isJob
  name
  schedules {
    id
    mode
    ...ScheduleSwitchFragment
    __typename
  }
  sensors {
    id
    targets {
      pipelineName
      mode
      __typename
    }
    ...SensorSwitchFragment
    __typename
  }
  __typename
}

fragment ScheduleSwitchFragment on Schedule {
  id
  name
  cronSchedule
  scheduleState {
    id
    status
    __typename
  }
  __typename
}

fragment SensorSwitchFragment on Sensor {
  id
  jobOriginId
  name
  sensorState {
    id
    status
    __typename
  }
  __typename
}

fragment RunMetadataFragment on PipelineRun {
  id
  status
  assets {
    id
    key {
      path
      __typename
    }
    __typename
  }
  ...RunTimeFragment
  __typename
}

fragment RunTimeFragment on Run {
  id
  runId
  status
  startTime
  endTime
  updateTime
  __typename
}"""


PipelineExplorerRootQuery="""query PipelineExplorerRootQuery($snapshotPipelineSelector: PipelineSelector, $snapshotId: String, $rootHandleID: String!, $requestScopeHandleID: String) {
  pipelineSnapshotOrError(
    snapshotId: $snapshotId
    activePipelineSelector: $snapshotPipelineSelector
  ) {
    ... on PipelineSnapshot {
      id
      name
      ...GraphExplorerFragment
      solidHandle(handleID: $rootHandleID) {
        ...GraphExplorerSolidHandleFragment
        __typename
      }
      solidHandles(parentHandleID: $requestScopeHandleID) {
        handleID
        solid {
          name
          definition {
            assetNodes {
              id
              ...GraphExplorerAssetNodeFragment
              __typename
            }
            __typename
          }
          __typename
        }
        ...GraphExplorerSolidHandleFragment
        __typename
      }
      __typename
    }
    ... on PipelineNotFoundError {
      message
      __typename
    }
    ... on PipelineSnapshotNotFoundError {
      message
      __typename
    }
    ... on PythonError {
      message
      __typename
    }
    __typename
  }
}

fragment GraphExplorerFragment on SolidContainer {
  id
  name
  description
  ...SidebarTabbedContainerPipelineFragment
  __typename
}

fragment SidebarTabbedContainerPipelineFragment on SolidContainer {
  id
  name
  ...SidebarOpContainerInfoFragment
  __typename
}

fragment SidebarOpContainerInfoFragment on SolidContainer {
  id
  name
  description
  modes {
    id
    ...SidebarModeInfoFragment
    __typename
  }
  __typename
}

fragment SidebarModeInfoFragment on Mode {
  id
  name
  description
  resources {
    name
    description
    configField {
      configType {
        ...ConfigTypeSchemaFragment
        recursiveConfigTypes {
          ...ConfigTypeSchemaFragment
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  loggers {
    name
    description
    configField {
      configType {
        ...ConfigTypeSchemaFragment
        recursiveConfigTypes {
          ...ConfigTypeSchemaFragment
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment ConfigTypeSchemaFragment on ConfigType {
  __typename
  ... on EnumConfigType {
    givenName
    __typename
  }
  ... on RegularConfigType {
    givenName
    __typename
  }
  key
  description
  isSelector
  typeParamKeys
  ... on CompositeConfigType {
    fields {
      name
      description
      isRequired
      configTypeKey
      __typename
    }
    __typename
  }
  ... on ScalarUnionConfigType {
    scalarTypeKey
    nonScalarTypeKey
    __typename
  }
  ... on MapConfigType {
    keyLabelName
    __typename
  }
}

fragment GraphExplorerSolidHandleFragment on SolidHandle {
  handleID
  solid {
    name
    ...PipelineGraphOpFragment
    __typename
  }
  __typename
}

fragment PipelineGraphOpFragment on Solid {
  name
  ...OpNodeInvocationFragment
  definition {
    name
    ...OpNodeDefinitionFragment
    __typename
  }
  __typename
}

fragment OpNodeInvocationFragment on Solid {
  name
  isDynamicMapped
  inputs {
    definition {
      name
      __typename
    }
    isDynamicCollect
    dependsOn {
      definition {
        name
        type {
          displayName
          __typename
        }
        __typename
      }
      solid {
        name
        __typename
      }
      __typename
    }
    __typename
  }
  outputs {
    definition {
      name
      __typename
    }
    dependedBy {
      solid {
        name
        __typename
      }
      definition {
        name
        type {
          displayName
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment OpNodeDefinitionFragment on ISolidDefinition {
  __typename
  name
  description
  metadata {
    key
    value
    __typename
  }
  assetNodes {
    id
    assetKey {
      path
      __typename
    }
    __typename
  }
  inputDefinitions {
    name
    type {
      displayName
      __typename
    }
    __typename
  }
  outputDefinitions {
    name
    isDynamic
    type {
      displayName
      __typename
    }
    __typename
  }
  ... on SolidDefinition {
    configField {
      configType {
        key
        description
        __typename
      }
      __typename
    }
    __typename
  }
  ... on CompositeSolidDefinition {
    id
    inputMappings {
      definition {
        name
        __typename
      }
      mappedInput {
        definition {
          name
          __typename
        }
        solid {
          name
          __typename
        }
        __typename
      }
      __typename
    }
    outputMappings {
      definition {
        name
        __typename
      }
      mappedOutput {
        definition {
          name
          __typename
        }
        solid {
          name
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment GraphExplorerAssetNodeFragment on AssetNode {
  id
  opName
  assetKey {
    path
    __typename
  }
  __typename
}
"""



JobOverviewSidebarQuery="""query JobOverviewSidebarQuery($pipelineSelector: PipelineSelector!) {
  pipelineSnapshotOrError(activePipelineSelector: $pipelineSelector) {
    ... on PipelineSnapshot {
      id
      name
      description
      modes {
        id
        ...SidebarModeInfoFragment
        __typename
      }
      __typename
    }
    ... on PipelineNotFoundError {
      message
      __typename
    }
    ... on PipelineSnapshotNotFoundError {
      message
      __typename
    }
    ... on PythonError {
      message
      __typename
    }
    __typename
  }
}

fragment SidebarModeInfoFragment on Mode {
  id
  name
  description
  resources {
    name
    description
    configField {
      configType {
        ...ConfigTypeSchemaFragment
        recursiveConfigTypes {
          ...ConfigTypeSchemaFragment
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  loggers {
    name
    description
    configField {
      configType {
        ...ConfigTypeSchemaFragment
        recursiveConfigTypes {
          ...ConfigTypeSchemaFragment
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment ConfigTypeSchemaFragment on ConfigType {
  __typename
  ... on EnumConfigType {
    givenName
    __typename
  }
  ... on RegularConfigType {
    givenName
    __typename
  }
  key
  description
  isSelector
  typeParamKeys
  ... on CompositeConfigType {
    fields {
      name
      description
      isRequired
      configTypeKey
      __typename
    }
    __typename
  }
  ... on ScalarUnionConfigType {
    scalarTypeKey
    nonScalarTypeKey
    __typename
  }
  ... on MapConfigType {
    keyLabelName
    __typename
  }
}"""


LaunchpadRootQuery="""query LaunchpadRootQuery($pipelineName: String!, $repositoryName: String!, $repositoryLocationName: String!) {
  pipelineOrError(
    params: {pipelineName: $pipelineName, repositoryName: $repositoryName, repositoryLocationName: $repositoryLocationName}
  ) {
    ... on PipelineNotFoundError {
      message
      __typename
    }
    ... on PythonError {
      message
      __typename
    }
    ... on Pipeline {
      id
      ...LaunchpadSessionContainerPipelineFragment
      __typename
    }
    __typename
  }
  partitionSetsOrError(
    pipelineName: $pipelineName
    repositorySelector: {repositoryName: $repositoryName, repositoryLocationName: $repositoryLocationName}
  ) {
    __typename
    ...LaunchpadSessionContainerPartitionSetsFragment
    ... on PipelineNotFoundError {
      message
      __typename
    }
    ... on PythonError {
      message
      __typename
    }
  }
}

fragment LaunchpadSessionContainerPipelineFragment on Pipeline {
  id
  isJob
  ...ConfigEditorGeneratorPipelineFragment
  modes {
    id
    name
    description
    __typename
  }
  __typename
}

fragment ConfigEditorGeneratorPipelineFragment on Pipeline {
  id
  isJob
  name
  presets {
    __typename
    name
    mode
    solidSelection
    runConfigYaml
    tags {
      key
      value
      __typename
    }
  }
  tags {
    key
    value
    __typename
  }
  __typename
}

fragment LaunchpadSessionContainerPartitionSetsFragment on PartitionSets {
  ...ConfigEditorGeneratorPartitionSetsFragment
  __typename
}

fragment ConfigEditorGeneratorPartitionSetsFragment on PartitionSets {
  results {
    id
    name
    mode
    solidSelection
    __typename
  }
  __typename
}"""


PipelineExecutionConfigSchemaQuery="""query PipelineExecutionConfigSchemaQuery($selector: PipelineSelector!, $mode: String) {
  runConfigSchemaOrError(selector: $selector, mode: $mode) {
    ...LaunchpadSessionContainerRunConfigSchemaFragment
    __typename
  }
}

fragment LaunchpadSessionContainerRunConfigSchemaFragment on RunConfigSchemaOrError {
  __typename
  ... on RunConfigSchema {
    ...ConfigEditorRunConfigSchemaFragment
    __typename
  }
  ... on ModeNotFoundError {
    message
    __typename
  }
}

fragment ConfigEditorRunConfigSchemaFragment on RunConfigSchema {
  rootConfigType {
    key
    __typename
  }
  allConfigTypes {
    __typename
    key
    description
    isSelector
    typeParamKeys
    ... on RegularConfigType {
      givenName
      __typename
    }
    ... on MapConfigType {
      keyLabelName
      __typename
    }
    ... on EnumConfigType {
      givenName
      values {
        value
        description
        __typename
      }
      __typename
    }
    ... on CompositeConfigType {
      fields {
        name
        description
        isRequired
        configTypeKey
        __typename
      }
      __typename
    }
    ... on ScalarUnionConfigType {
      key
      scalarTypeKey
      nonScalarTypeKey
      __typename
    }
  }
  __typename
}"""


OpSelectorQuery="""query OpSelectorQuery($selector: PipelineSelector!, $requestScopeHandleID: String) {
  pipelineOrError(params: $selector) {
    __typename
    ... on Pipeline {
      id
      name
      solidHandles(parentHandleID: $requestScopeHandleID) {
        handleID
        solid {
          name
          __typename
        }
        ...GraphExplorerSolidHandleFragment
        __typename
      }
      __typename
    }
    ... on PipelineNotFoundError {
      message
      __typename
    }
    ... on InvalidSubsetError {
      message
      __typename
    }
    ... on PythonError {
      message
      __typename
    }
  }
}

fragment GraphExplorerSolidHandleFragment on SolidHandle {
  handleID
  solid {
    name
    ...PipelineGraphOpFragment
    __typename
  }
  __typename
}

fragment PipelineGraphOpFragment on Solid {
  name
  ...OpNodeInvocationFragment
  definition {
    name
    ...OpNodeDefinitionFragment
    __typename
  }
  __typename
}

fragment OpNodeInvocationFragment on Solid {
  name
  isDynamicMapped
  inputs {
    definition {
      name
      __typename
    }
    isDynamicCollect
    dependsOn {
      definition {
        name
        type {
          displayName
          __typename
        }
        __typename
      }
      solid {
        name
        __typename
      }
      __typename
    }
    __typename
  }
  outputs {
    definition {
      name
      __typename
    }
    dependedBy {
      solid {
        name
        __typename
      }
      definition {
        name
        type {
          displayName
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment OpNodeDefinitionFragment on ISolidDefinition {
  __typename
  name
  description
  metadata {
    key
    value
    __typename
  }
  assetNodes {
    id
    assetKey {
      path
      __typename
    }
    __typename
  }
  inputDefinitions {
    name
    type {
      displayName
      __typename
    }
    __typename
  }
  outputDefinitions {
    name
    isDynamic
    type {
      displayName
      __typename
    }
    __typename
  }
  ... on SolidDefinition {
    configField {
      configType {
        key
        description
        __typename
      }
      __typename
    }
    __typename
  }
  ... on CompositeSolidDefinition {
    id
    inputMappings {
      definition {
        name
        __typename
      }
      mappedInput {
        definition {
          name
          __typename
        }
        solid {
          name
          __typename
        }
        __typename
      }
      __typename
    }
    outputMappings {
      definition {
        name
        __typename
      }
      mappedOutput {
        definition {
          name
          __typename
        }
        solid {
          name
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}"""


LaunchPipelineExecution="""mutation LaunchPipelineExecution($executionParams: ExecutionParams!) {
  launchPipelineExecution(executionParams: $executionParams) {
    __typename
    ... on LaunchRunSuccess {
      run {
        id
        runId
        pipelineName
        __typename
      }
      __typename
    }
    ... on PipelineNotFoundError {
      message
      __typename
    }
    ... on RunConfigValidationInvalid {
      errors {
        message
        __typename
      }
      __typename
    }
    ... on PythonError {
      message
      stack
      __typename
    }
  }
}"""


RunsRootQuery="""query RunsRootQuery($limit: Int, $cursor: String, $filter: RunsFilter!, $queuedFilter: RunsFilter!, $inProgressFilter: RunsFilter!) {
  pipelineRunsOrError(limit: $limit, cursor: $cursor, filter: $filter) {
    ... on Runs {
      results {
        id
        ...RunTableRunFragment
        __typename
      }
      __typename
    }
    ... on InvalidPipelineRunsFilterError {
      message
      __typename
    }
    ... on PythonError {
      message
      __typename
    }
    __typename
  }
  queuedCount: pipelineRunsOrError(filter: $queuedFilter) {
    ...CountFragment
    __typename
  }
  inProgressCount: pipelineRunsOrError(filter: $inProgressFilter) {
    ...CountFragment
    __typename
  }
}

fragment RunTableRunFragment on Run {
  id
  runId
  status
  stepKeysToExecute
  canTerminate
  mode
  rootRunId
  parentRunId
  pipelineSnapshotId
  pipelineName
  repositoryOrigin {
    id
    repositoryName
    repositoryLocationName
    __typename
  }
  solidSelection
  status
  tags {
    key
    value
    __typename
  }
  ...RunTimeFragment
  __typename
}

fragment RunTimeFragment on Run {
  id
  runId
  status
  startTime
  endTime
  updateTime
  __typename
}

fragment CountFragment on Runs {
  count
  __typename
}"""


InstanceSchedulesQuery="""query InstanceSchedulesQuery {
  instance {
    ...InstanceHealthFragment
    __typename
  }
  repositoriesOrError {
    __typename
    ... on RepositoryConnection {
      nodes {
        id
        name
        ...RepositoryInfoFragment
        schedules {
          id
          ...ScheduleFragment
          __typename
        }
        __typename
      }
      __typename
    }
    ...PythonErrorFragment
  }
  unloadableInstigationStatesOrError {
    ... on InstigationStates {
      results {
        id
        ...InstigationStateFragment
        __typename
      }
      __typename
    }
    ...PythonErrorFragment
    __typename
  }
}

fragment InstanceHealthFragment on Instance {
  daemonHealth {
    id
    ...DaemonHealthFragment
    __typename
  }
  hasInfo
  __typename
}

fragment DaemonHealthFragment on DaemonHealth {
  id
  allDaemonStatuses {
    id
    daemonType
    required
    healthy
    lastHeartbeatErrors {
      __typename
      ...PythonErrorFragment
    }
    lastHeartbeatTime
    __typename
  }
  __typename
}

fragment PythonErrorFragment on PythonError {
  __typename
  message
  stack
  cause {
    message
    stack
    __typename
  }
}

fragment RepositoryInfoFragment on Repository {
  id
  name
  location {
    id
    name
    __typename
  }
  displayMetadata {
    key
    value
    __typename
  }
  __typename
}

fragment ScheduleFragment on Schedule {
  id
  name
  cronSchedule
  executionTimezone
  pipelineName
  solidSelection
  mode
  description
  partitionSet {
    id
    name
    __typename
  }
  scheduleState {
    id
    ...InstigationStateFragment
    __typename
  }
  futureTicks(limit: 5) {
    results {
      timestamp
      __typename
    }
    __typename
  }
  __typename
}

fragment InstigationStateFragment on InstigationState {
  id
  name
  instigationType
  status
  repositoryOrigin {
    id
    ...RepositoryOriginFragment
    __typename
  }
  typeSpecificData {
    ... on SensorData {
      lastRunKey
      __typename
    }
    ... on ScheduleData {
      cronSchedule
      __typename
    }
    __typename
  }
  runs(limit: 1) {
    id
    runId
    status
    __typename
  }
  status
  ticks(limit: 1) {
    id
    ...TickTagFragment
    __typename
  }
  runningCount
  __typename
}

fragment RepositoryOriginFragment on RepositoryOrigin {
  id
  repositoryLocationName
  repositoryName
  repositoryLocationMetadata {
    key
    value
    __typename
  }
  __typename
}

fragment TickTagFragment on InstigationTick {
  id
  status
  timestamp
  skipReason
  runIds
  error {
    ...PythonErrorFragment
    __typename
  }
  __typename
}"""


InstanceSensorsQuery="""query InstanceSensorsQuery {
  instance {
    ...InstanceHealthFragment
    __typename
  }
  repositoriesOrError {
    __typename
    ... on RepositoryConnection {
      nodes {
        id
        name
        ...RepositoryInfoFragment
        sensors {
          id
          ...SensorFragment
          __typename
        }
        __typename
      }
      __typename
    }
    ...PythonErrorFragment
  }
  unloadableInstigationStatesOrError {
    ... on InstigationStates {
      results {
        id
        ...InstigationStateFragment
        __typename
      }
      __typename
    }
    ...PythonErrorFragment
    __typename
  }
}

fragment InstanceHealthFragment on Instance {
  daemonHealth {
    id
    ...DaemonHealthFragment
    __typename
  }
  hasInfo
  __typename
}

fragment DaemonHealthFragment on DaemonHealth {
  id
  allDaemonStatuses {
    id
    daemonType
    required
    healthy
    lastHeartbeatErrors {
      __typename
      ...PythonErrorFragment
    }
    lastHeartbeatTime
    __typename
  }
  __typename
}

fragment PythonErrorFragment on PythonError {
  __typename
  message
  stack
  cause {
    message
    stack
    __typename
  }
}

fragment RepositoryInfoFragment on Repository {
  id
  name
  location {
    id
    name
    __typename
  }
  displayMetadata {
    key
    value
    __typename
  }
  __typename
}

fragment SensorFragment on Sensor {
  id
  jobOriginId
  name
  description
  minIntervalSeconds
  nextTick {
    timestamp
    __typename
  }
  sensorState {
    id
    ...InstigationStateFragment
    __typename
  }
  targets {
    pipelineName
    solidSelection
    mode
    __typename
  }
  metadata {
    assetKeys {
      path
      __typename
    }
    __typename
  }
  __typename
}

fragment InstigationStateFragment on InstigationState {
  id
  name
  instigationType
  status
  repositoryOrigin {
    id
    ...RepositoryOriginFragment
    __typename
  }
  typeSpecificData {
    ... on SensorData {
      lastRunKey
      __typename
    }
    ... on ScheduleData {
      cronSchedule
      __typename
    }
    __typename
  }
  runs(limit: 1) {
    id
    runId
    status
    __typename
  }
  status
  ticks(limit: 1) {
    id
    ...TickTagFragment
    __typename
  }
  runningCount
  __typename
}

fragment RepositoryOriginFragment on RepositoryOrigin {
  id
  repositoryLocationName
  repositoryName
  repositoryLocationMetadata {
    key
    value
    __typename
  }
  __typename
}

fragment TickTagFragment on InstigationTick {
  id
  status
  timestamp
  skipReason
  runIds
  error {
    ...PythonErrorFragment
    __typename
  }
  __typename
}"""


StopSensor="""mutation StopSensor($jobOriginId: String!) {
  stopSensor(jobOriginId: $jobOriginId) {
    __typename
    ... on StopSensorMutationResult {
      instigationState {
        id
        status
        __typename
      }
      __typename
    }
    ... on PythonError {
      message
      stack
      __typename
    }
  }
}"""


StartSensor="""mutation StartSensor($sensorSelector: SensorSelector!) {
  startSensor(sensorSelector: $sensorSelector) {
    __typename
    ... on Sensor {
      id
      sensorState {
        id
        status
        __typename
      }
      __typename
    }
    ... on PythonError {
      message
      stack
      __typename
    }
  }
}"""


InstanceHealthQuery="""query InstanceHealthQuery {
  instance {
    ...InstanceHealthFragment
    __typename
  }
}

fragment InstanceHealthFragment on Instance {
  daemonHealth {
    id
    ...DaemonHealthFragment
    __typename
  }
  hasInfo
  __typename
}

fragment DaemonHealthFragment on DaemonHealth {
  id
  allDaemonStatuses {
    id
    daemonType
    required
    healthy
    lastHeartbeatErrors {
      __typename
      ...PythonErrorFragment
    }
    lastHeartbeatTime
    __typename
  }
  __typename
}

fragment PythonErrorFragment on PythonError {
  __typename
  message
  stack
  cause {
    message
    stack
    __typename
  }
}"""


InstanceConfigQuery="""query InstanceConfigQuery {
  version
  instance {
    info
    __typename
  }
}"""



ReloadRepositoryLocationMutation="""mutation ReloadRepositoryLocationMutation($location: String!) {
  reloadRepositoryLocation(repositoryLocationName: $location) {
    __typename
    ... on WorkspaceLocationEntry {
      id
      __typename
    }
    ... on UnauthorizedError {
      message
      __typename
    }
    ... on ReloadNotSupported {
      message
      __typename
    }
    ... on RepositoryLocationNotFound {
      message
      __typename
    }
    ... on PythonError {
      ...PythonErrorFragment
      __typename
    }
  }
}

fragment PythonErrorFragment on PythonError {
  __typename
  message
  stack
  cause {
    message
    stack
    __typename
  }
}"""


"""mutation Delete($runId: String!) {
  deletePipelineRun(runId: $runId) {
    __typename
    ... on PythonError {
      message
      __typename
    }
    ... on UnauthorizedError {
      message
      __typename
    }
    ... on RunNotFoundError {
      message
      __typename
    }
  }
}"""
