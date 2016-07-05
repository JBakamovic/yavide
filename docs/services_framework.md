# Contents
* [Framework](#framework)
* [Services](#services)
  * [Syntax highlighting](#syntax-highlighting)
  * [Indexing](#indexing)
  * [Auto-formatting](#auto-formatting)
  * [Project builder](#project-builder)
* [How to enable/disable service](#how-to-enabledisable-service)

# Framework
Naturally, one does not want to block the main UI thread and obstruct the user workflow while doing some lenghty operations. Lengthy operations are 
are quite ubiquitous in development environments and as a matter of fact a lot of processing has to be done in background with or without user awareness 
in order to bring the best experience. As `Vim` did not really have native support for asynchronous processing (only recently some async support has been added?), 
a custom solution had to been brought in.

Therefore, to ease the development and integration of any kind of lengthy operations this framework has been developed. In the context of this framework 
lenghty operations are encapsulated in units called `services`. Each [`service`](../core/services/yavide_service.py):
  * Has its own unique ID
  * Is dispatched to its own background process
  * Can be started and shut down on request
  * Can be triggered at any moment during its runtime
  * Can notify the main thread about its events and queue the actions to be executed on the UI side

To make the communication between the UI and background `services` seamless, [`YavideServer`](../core/server/yavide_server.py) on the server side and [`Y_Server...()` API](../core/.api.vimrc) 
on the client side is taking care of that. `YavideServer` is a thin proxy layer which controls and handles all the `services`.

Important aspect of this framework is that it provides a generic `service` development platform and enables `service` developer to fully focus on the 
implementation details of particular `service`. See existing `services` to see an example how implementation may look like.

# Services

## Syntax highlighting
TBD

Compared to the limited `Vim` syntax highlighting mechanism, this service brings more complete syntax highlighting including support for the following symbols:
* Namespaces
* Classes
* Structures
* Enums
* Enum values
* Unions
* Class/struct members
* Local variables
* Variable definitions
* Function prototypes
* Function definitions
* Macros
* Typedefs
* Forward declarations

As of now `ctags` is being used as a back-end for syntax highlighting which falls short in some cases which is why it is planned to replace it by the `clang`-based solution to get more complete and more precise results.

Before | After
-------|--------
![Syntax highlighting before](https://raw.githubusercontent.com/wiki/JBakamovic/yavide/images/syntax_highlighting_before.png) | ![Syntax highlighting after](https://raw.githubusercontent.com/wiki/JBakamovic/yavide/images/syntax_highlighting_after.png) 

## Indexing
TBD

Similar as with syntax highlighting but in addition `cscope` is also used. 

![Indexer in action](https://raw.githubusercontent.com/wiki/JBakamovic/yavide/images/indexer_in_action.gif)

## Auto-formatting
TBD

Create `.clang-format` config file in the project root directory. Auto-formatting is being triggered upon each `SaveFile` action. 
In future this will be a matter of configuration. Currently it is hard-coded in this way.

![Auto-formatter in action](https://raw.githubusercontent.com/wiki/JBakamovic/yavide/images/auto_formatter_in_action.gif)

## Project builder
TBD

Set `g:project_env_build_command` to the build command specific to the project. I.e. after loading/importing the project do the following:  
  * `let g:project_env_build_command='make all'`

Once this variable has been successfully set, one is able to use `YavideBuildRun` command or `F7` to trigger the build.
Upon completion `quickfix` window will be populated with build output where in case of any warnings/errors one is able
to jump to the given warning/error double-clicking/pressing-enter-key on the particular entry from the list. Once the project has 
been saved build command will be persisted in project settings and therefore re-loaded on the next project start-up.

Current progress of the build cannot be tracked directly from `Yavide` but one can use `tail -f /tmp/yavide<random_string>build` from the terminal. 
Possibility to stream the build directly on-the-fly to the `Yavide` environment (i.e. `quickfix` window) needs to be evaluated and will be considered.

![Building the project](https://raw.githubusercontent.com/wiki/JBakamovic/yavide/images/build_in_action.gif)

# How to enable/disable service

Set `enabled` property to 0 or 1 corresponding to the service which you want to enable/disable. Property can be found as
part of the `g:project_service_<service_name>` variable which is defined in `<yavide_install_dir>/core/.globals.vimrc`.

