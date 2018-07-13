" --------------------------------------------------------------------------------------------------------------------------------------
"
"   Global (vim) variables
"
" --------------------------------------------------------------------------------------------------------------------------------------
let g:project_configuration_filename      = '.yavide_proj'
let g:project_session_filename            = '.yavide_session'
let g:project_loaded                      = 0
let g:project_root_directory              = ''
let g:project_env_compilation_db_path     = ''
let g:project_env_build_preproces_command = ''
let g:project_env_build_command           = ''

let g:project_category_generic          = { 'id' : 1 }
let g:project_category_makefile         = { 'id' : 2 }
let g:project_supported_categories      = {
\                                           'Generic'   :   g:project_category_generic,
\                                           'Makefile'  :   g:project_category_makefile
\}

let g:project_compilation_db_json       = { 'id' : 1, 'name' : 'compile_commands.json', 'description' : 'JSON Compilation DB' }
let g:project_compilation_db_simple_txt = { 'id' : 2, 'name' : 'compile_flags.txt',     'description' : 'Simple txt file containing compiler flags' }
let g:project_supported_compilation_db  = {
\                                           'json' : g:project_compilation_db_json,
\                                           'txt'  : g:project_compilation_db_simple_txt,
\}

let g:project_type_generic              = { 'id' : 1, 'extensions' : ['.*'] }
let g:project_type_c                    = { 'id' : 2, 'extensions' : ['.c', '.h'] }
let g:project_type_cpp                  = { 'id' : 3, 'extensions' : ['.cpp', '.cc', '.h', '.hh', '.hpp'] }
let g:project_type_java                 = { 'id' : 4, 'extensions' : ['.java'] }
let g:project_type_mixed                = { 'id' : 5, 'extensions' : [] }
let g:project_supported_types           = {
\                                           'Generic'   :   g:project_type_generic,
\                                           'C'         :   g:project_type_c,
\                                           'C++'       :   g:project_type_cpp,
\                                           'Mixed'     :   g:project_type_mixed,
\}

