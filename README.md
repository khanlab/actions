# Khanlab Github Actions

A central repository storing reusable workflows and composite actions for
Github actions, enabling simpler maintenance of workflows across
different projects.

## Composite action

Composite actions (stored in `.github/actions`) are non-specific, reusable
tasks (e.g. grabbing a project version, making a commit). These can be
inserted as a step within a job in a downstream workflow.

The name of the composite action is defined by the directory name. The
intended steps are stored within an `action.yml` file within each directory.

## Reusable workflow

Resuable workflows (stored in `.github/workflows`) are intended to perform a
specific task (e.g. deploy a docker container, assign a reviewer, etc). These
can only be called as a "job" in the downstream action.

The name of the reusable workflows is defined directly within the `workflows`
directory.

## Contributing

Everyone is welcome to contribute their resuable workflows and composite
actions. If using a composite action within a reusable workflow, the
`org/repo` must be specified, otherwise downstream usage will assume the
composite action is stored within the downstream repository.

An example of this can be seen below:

```yaml
- name: Grab previous version
  id: semver
  uses: khanlab/actions/.github/actions/action-version_task-updatePrereleaseVersion@v0.2.2
  with:
    project-metadata: ${{ inputs.project-metadata }}
    bp-pat: ${{ secrets.BP_PAT }}
```

Naming of these files take inspiration from BIDS, but with a camel-case
value scheme. Workflows are defined by the `workflow` entity, while composite
actions are defined by the `action` entity. The intended task is defined by
`task`.

_NOTE: You can test your workflow locally using a tool like_
_[nektos/act](https://github.com/nektos/act). For security reasons, it is_
_recommended to include your secrets in an external file."_
