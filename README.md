# ansible_tower_genie_collections
![Ansible Lint](https://github.com/redhat-cop/automate_tower_genie_collections/workflows/Ansible%20Lint/badge.svg)

# Foo Collection
<!-- Add CI and code coverage badges here. Samples included below. -->
[![CI](https://github.com/ansible-collections/REPONAMEHERE/workflows/CI/badge.svg?event=push)](https://github.com/ansible-collections/REPONAMEHERE/actions) [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/REPONAMEHERE)](https://codecov.io/gh/ansible-collections/REPONAMEHERE)

<!-- Describe the collection and why a user would want to use it. What does the collection do? -->

This is a collection of roles for AWX/Tower.

## Release Process
This collection uses an auatomated GitHub workflow to publish releases to Ansible Galaxy. This workflow can be found in `.github/workflows/galaxy-release.yml`. It is dependent on `release.yml` and `galaxy.yml.j2`. See instructions below for usage.

To publish a release to Galaxy:
1) An administrator of the repository must configure a secret in the settings containing the API key for the Galaxy namespace. The secret should be called `ANSIBLE_GALAXY_APIKEY`. This is a one time step.
2) To publish a release, click "releases" at the top of repository home page and "Draft a new release"
3) The "Tag version" should be in the form `v#.#.#`. A suffix may be added such as `-dev#` or `rc#` for pre-releases. These will still publish to Galaxy but will not be chosen when installing `latest`. The version must be explicitly stated when installing to use pre-releases.
4) Title the release, it is recommended to use the "Tag version"
5) Clicking "Publish release" will initiate the workflow. If there are no errors building the collection, it will be automatically published to galaxy as the version suppied for "Tag version"

## Tested with Ansible

<!-- List the versions of Ansible the collection has been tested with. Must match what is in galaxy.yml. -->

## External requirements

This collection depends on the awx.collection since it uses the modules there.

### Supported connections
<!-- Optional. If your collection supports only specific connection types (such as HTTPAPI, netconf, or others), list them here. -->

## Included content

<!-- Galaxy will eventually list the module docs within the UI, but until that is ready, you may need to either describe your plugins etc here, or point to an external docsite to cover that information. -->

## Using this collection

<!--Include some quick examples that cover the most common use cases for your collection content. -->

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

<!--Describe how the community can contribute to your collection. At a minimum, include how and where users can create issues to report problems or request features for this collection.  List contribution requirements, including preferred workflows and necessary testing, so you can benefit from community PRs. If you are following general Ansible contributor guidelines, you can link to - [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html). -->


## Release notes
<!--Add a link to a changelog.md file or an external docsite to cover this information. -->

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

<!-- Include the appropriate license information here and a pointer to the full licensing details. If the collection contains modules migrated from the ansible/ansible repo, you must use the same license that existed in the ansible/ansible repo. See the GNU license example below. -->

GNU General Public License v3.0 or later.

See [LICENCE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
