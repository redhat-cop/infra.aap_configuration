======================================
infra.eda\_configuration Release Notes
======================================

.. contents:: Topics

v1.1.0
======

Minor Changes
-------------

- Added eda_api lookup plugin

Bugfixes
--------

- Fix issue where wrong not checking for full match of name when searching for existing objects
- Fixes issue where project sync reports fail because it is already running

v1.0.0
======

Major Changes
-------------

- Add dispatch role
- Added credential module
- Added credential role
- Added decision environment module
- Added decision environment role
- Added project module
- Added project role
- Added project_sync module
- Added project_sync role
- Added rulebook_activation module
- Added rulebook_activation role
- Added user module
- Added user role
- Added user_token module
- Added user_token role

Bugfixes
--------

- Fixed error message when project sync fails
- fixed a bug where resolve_name_to_id data was not defined
- fixed a bug with the API returning multiple items because it only matches the name starting with the value
