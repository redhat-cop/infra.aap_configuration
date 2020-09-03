# How to Contribute

We welcome contributions from the community. Here are a few ways you can help us improve.

## Open an Issue

If you see something you'd like changed, but aren't sure how to change it, submit an issue describing what you'd like to see.

## Working Locally
Ensure you install the awx collections, so that roles and playbooks can be properly linted:
`ansible-galaxy collection install awx.awx -p collections/`

Python's pre-commit tool can be installed, and hooks installed, to cleanup whitespace, newlines, and run yamllint and ansible-lint against your local changes before committing. This will help you avoid failures in the github workflows.

1. Create a local virtual environment for tower_configurations (suggested, its your system!)
2. Use pip to install pre-commit in your environment of choice: `pip install pre-commit`
3. Install pre-commit hooks with `pre-commit install --install-hooks -c .github/workflow-config/.pre-commit-config.yml`
4. With hooks installed, they will be run automatically when you call `git commit`, blocking commit if any hooks fail.
5. [Optional] If you want to ignore hook failures and commit anyway, use `git commit -n`
6. [Optional] Run pre-commit checks at any time with `pre-commit run --all -c .github/workflow-config/.pre-commit-config.yml`.

Please see pre-commit documentation for further explanation: [Pre-commit](https://pre-commit.com/)

## Submit a Pull Request

If you feel like getting your hands dirty, feel free to make the change yourself. Here's how:

1. Fork the repo on Github, and then clone it locally.
2. Create a branch named appropriately for the change you are going to make.
3. Make your code change.
4. If you are creating a new role, please add a test for it in our [testing playbook.](https://github.com/redhat-cop/tower_configuration/blob/devel/playbooks/example_with_yaml/configure_tower.yml) by adding a new role entry and adding the appropriate yaml file with test data in the tower_configs directory.
5. Add a changelog fragment in `changelogs/fragments` as per https://docs.ansible.com/ansible/latest/community/development_process.html#changelogs
6. Push your code change up to your forked repo.
7. Open a Pull Request to merge your changes to this repo. The comment box will be filled in automatically via a template.
8. All Pull Requests will be subject to Ansible and Yaml Linting checks. Please make sure that your code complies and fix any warnings that arise. These are Checks that apear at the bottom of your Pull Request.
9. All Pull requests are subject to Testing against being used in tower. As above there is a check at the bottom of your pull request for this named integration.

See [Using Pull Requests](https://help.github.com/articles/using-pull-requests/) got more information on how to use GitHub PRs.

For an in depth guide on how to contribute see [this article](https://opensource.com/article/19/7/create-pull-request-github)
