Ventor Base
=========================

Base module that allow relation between Ventor modules

Changelog
---------

13.0.1.3.10 (2022-05-31)
***********************

* Fixed uploading Custom Mobile Logo

13.0.1.3.9 (2022-04-27)
***********************

* Added 'Operation Type' field and logic of validation to Batch Transfer
* Changed name of the group from 'Manufacturing Menu' to 'MO and WO management'
* Added updating warehouse_id for all locations to ventor base in post_hook and migration
* Added record rules 'See Stock Quant Package from allowed warehouses' and 
  'See Stock Inventory Lines from allowed warehouses' for restricting access to warehouses for odoo users

13.0.1.3.8 (2022-02-03)
***********************

* Added security group 'Warehouse Operations: Allow applying all qty of product'
* Added automatic switch on the 'Manage package' setting in all menus to default if setting "Package" is switched on
* Added the setting “Scan destination location” to all Operation Types
* Added dependency of settings 'Show next product' and 'Confirm product'
* Added the settings 'Behavior on split operation' and 'Behavior on backorder creation' to all Operation Types
* Added post init hook and migration for setup Allowed Warehouses to users

13.0.1.3.7 (2021-12-2)
***********************

* [REM] Removed unused settings displayed in the Ventor Preferences tab on the user form
* [REM] Removed 'Default inventory location' from the Inventory settings from the Ventor Configuration
* [IMP] Changed 'Ventor Configuration' menu, added 'User Settings' menu item
* [REM] Removed 'Custom package name' field displayed in the Ventor Preferences tab on the user form
* [IMP] Added 'Custom Build Name' field in Ventor Configuration/Additional Settings
