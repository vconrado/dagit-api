from dagster.core.storage.pipeline_run import PipelineRunStatus


def safe_gets(data, paths):
    result = data
    for p in paths:
        result = result.get(p, {})
    return result

def to_run_status(result):
    if result.get("pipelineRunOrError", {}).get("__typename") != "Run":
            raise Exception(result)
        
    return PipelineRunStatus(result.get("pipelineRunOrError", {}).get("status", None))