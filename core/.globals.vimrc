" --------------------------------------------------------------------------------------------------------------------------------------
"
"   Global (vim) variables
"
" --------------------------------------------------------------------------------------------------------------------------------------
let g:project_configuration_filename      = '.yavide_proj'
let g:project_autocomplete_filename       = '.clang_complete'
let g:project_session_filename            = '.yavide_session'
let g:project_loaded                      = 0
let g:project_java_tags                   = ''
let g:project_java_tags_filename          = '.java_tags'
let g:project_cxx_tags                    = ''
let g:project_cxx_tags_filename           = '.cxx_tags'
let g:project_cscope_db_filename          = 'cscope.out'
let g:project_root_directory              = ''
let g:project_compiler_args               = ''
let g:project_env_build_preproces_command = ''
let g:project_env_build_command           = ''
let g:project_env_src_code_format_config  = '.clang-format'

let g:project_category_generic          = { 'id' : 1 }
let g:project_category_makefile         = { 'id' : 2 }
let g:project_supported_categories      = {
\                                           'Generic'   :   g:project_category_generic,
\                                           'Makefile'  :   g:project_category_makefile
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

" --------------------------------------------------------------------------------------------------------------------------------------
"
"   Services
"
" --------------------------------------------------------------------------------------------------------------------------------------
let g:project_service_src_code_model       = { 'id' : 0, 'enabled' : 1, 'start' : function("Y_SrcCodeModel_Start"), 'stop' : function("Y_SrcCodeModel_Stop"),
\                                              'services' : {
\                                                   'indexer'                   : { 'id' : 0, 'enabled' : 1 },
\                                                   'semantic_syntax_highlight' : { 'id' : 1, 'enabled' : 1 },
\                                                   'diagnostics'               : { 'id' : 2, 'enabled' : 1 },
\                                                   'type_deduction'            : { 'id' : 3, 'enabled' : 1 }
\                                               }
\                                            }
let g:project_service_project_builder      = { 'id' : 1, 'enabled' : 1, 'start' : function("Y_ProjectBuilder_Start"), 'stop' : function("Y_ProjectBuilder_Stop") }
let g:project_service_src_code_formatter   = { 'id' : 2, 'enabled' : 1, 'start' : function("Y_SrcCodeFormatter_Start"), 'stop' : function("Y_SrcCodeFormatter_Stop") }
let g:project_available_services           = [
\                                               g:project_service_src_code_model,
\                                               g:project_service_project_builder,
\                                               g:project_service_src_code_formatter
\]

" --------------------------------------------------------------------------------------------------------------------------------------
"
"   Global (python) variables
"
" --------------------------------------------------------------------------------------------------------------------------------------
python << EOF
from multiprocessing import Queue
server_queue = Queue()
EOF

