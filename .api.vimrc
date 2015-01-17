" --------------------------------------------------------------------------------------------------------------------------------------
"
"	Global variables
" 
" --------------------------------------------------------------------------------------------------------------------------------------
let g:project_configuration_filename	= ".yavide_proj"
let g:project_autocomplete_filename     = ".clang_complete"
let g:project_java_tags 				= ""
let g:project_java_tags_filename		= ".java_tags"
let g:project_cxx_tags 					= ""
let g:project_cxx_tags_filename			= ".cxx_tags"
let g:project_cscope_db_filename		= "cscope.out"
let g:project_supported_categories      = {
\                                           'Generic'   :   1,
\                                           'Makefile'  :   2
\}
let g:project_supported_types           = {
\                                           'Generic'   :   1,
\                                           'C'         :   2,
\                                           'C++'       :   3,
\                                           'Mixed'     :   4,
\                                           'Existing'  :   5
\}


" --------------------------------------------------------------------------------------------------------------------------------------
"
"	ENVIRONMENT INIT/DEINIT API
" 
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_Env_Init()
" Description:	Initializes the environment. Loads project specific settings.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Env_Init()
	execute('source ' . g:project_configuration_filename)
	let g:project_java_tags		 = g:project_full_path . '/' . g:project_java_tags_filename
	let g:project_cxx_tags 		 = g:project_full_path . '/' . g:project_cxx_tags_filename
    call Y_CScope_Init()
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_Env_Deinit()
" Description:	Deinitializes the environment.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Env_Deinit()
endfunction

" --------------------------------------------------------------------------------------------------------------------------------------
"
"	PROJECT MANAGEMENT API
" 
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Project_New()
	" Clean up all windows, buffers, previous sessions ...
	:CloseSession!

    " Ask user to provide project category
    let l:category_list = ['Project category:']
    for [category, category_id] in items(g:project_supported_categories)
        let l:cat_string = category_id . ' ' . category
        call add(l:category_list, cat_string)
    endfor
    call inputsave()
    let l:project_category = inputlist(l:category_list)
    call inputrestore()

    echo ' '

    if l:project_category > 0
        " Ask user to provide project type
        let l:type_list = ['Project type:']
        for [type, type_id] in items(g:project_supported_types)
            let l:type_string = type_id . ' ' . type
            call add(l:type_list, type_string)
        endfor
        call inputsave()
        let l:project_type = inputlist(l:type_list)
        call inputrestore()

        if l:project_type > 0
            " Ask user to provide a project root directory
            call inputsave()
            let l:project_root_directory = input('Enter project root directory: ', '', 'file')
            call inputrestore()

            if l:project_root_directory != ""
                " Ask user to provide a project name
                call inputsave()
                let l:project_name = input('Enter project name: ')
                call inputrestore()

                if l:project_name != ""
	                " Create project root directory
                    let l:curr_dir = getcwd()
                    let l:project_root_directory = l:curr_dir . '/' . l:project_root_directory
                    let l:project_full_path = l:project_root_directory . '/' . l:project_name
                    call mkdir(l:project_full_path, "p")
                    execute('cd ' . l:project_full_path)

                    " Create project specific files
                    call system('touch ' . g:project_configuration_filename)
                    call system('touch ' . g:project_autocomplete_filename)
                    if (l:project_category == g:project_supported_categories['Makefile'])
                        call system('touch ' . 'Makefile')
                    endif

                    " Store project specific settings into the project configuration file
                    let l:project_settings = []
                    call add(l:project_settings, 'let g:' . 'project_root_directory = ' . "\'" . l:project_root_directory . "\'")
                    call add(l:project_settings, 'let g:' . 'project_name = ' . "\'" . l:project_name . "\'")
                    call add(l:project_settings, 'let g:' . 'project_full_path = ' . "\'" . l:project_full_path . "\'")
                    call add(l:project_settings, 'let g:' . 'project_category = ' . l:project_category)
                    call add(l:project_settings, 'let g:' . 'project_type = ' . l:project_type)
                    call writefile(l:project_settings, g:project_configuration_filename)

                    " Initialize project specific stuff
                    call Y_Env_Init()

                    " Restore the layout
                    call Y_Layout_Refresh()

                    " Finally, save project into the new session
                    execute('SaveSession! ' . g:project_name)
                endif
            endif
        endif
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Project_Add()
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Project_Open()
	:OpenSession!
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Project_Close()
	:CloseSession!
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Project_Save()
	:SaveSession!
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Project_Delete()
    " TODO ask user if he wants to delete the project directory as well
    :DeleteSession!
endfunction


" --------------------------------------------------------------------------------------------------------------------------------------
"
"	SEARCH API
" 
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Prompt_Find()
	:promptfind
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Prompt_FindAndReplace()
	:promptrepl
endfunction


" --------------------------------------------------------------------------------------------------------------------------------------
"
"	BUFFER MANAGEMENT API
" 
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Buffer_Save()
	:w
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Buffer_Close()
	call Y_Buffer_GoTo(0) | sp | call Y_Buffer_GoTo(1) | bd
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Buffer_GoTo(bGoToNext)
    if &buftype != 'nofile' && &buftype != 'quickfix' && &buftype != 'help'
	    let cmd = a:bGoToNext == 1 ? ":bnext" : ":bprevious"
	    exec cmd
	    if &buftype ==# 'quickfix'
		    exec cmd
        endif
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Buffer_Scroll(bScrollDown)
	if (a:bScrollDown == 1)
		execute("normal \<C-e>")
	else
		execute("normal \<C-y>")
	endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_Buffer_StripTrailingWhitespaces()
" Description:	Strips trailing whitespaces from current buffer
" Dependency:	None
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Buffer_StripTrailingWhitespaces()
    " Preparation: save last search, and cursor position.
    let _s=@/
    let l = line(".")
    let c = col(".")
    " Do the business:
    %s/\s\+$//e
    " Clean up: restore previous search history, and cursor position
    let @/=_s
    call cursor(l, c)
endfunction


" --------------------------------------------------------------------------------------------------------------------------------------
"
"	TEXT MANAGEMENT API
" 
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Text_SelectAll()
	execute('normal ggVG')
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Text_Cut()
	execute('normal \"+x')
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Text_Copy()
	execute('normal \"+y')
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Text_Paste()
	execute('normal +gP')
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Text_Undo()
	execute('normal u')
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:
" Description:
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Text_Redo()
endfunction


" --------------------------------------------------------------------------------------------------------------------------------------
"
"	SOURCE CODE NAVIGATION API
" 
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcNav_OpenFile()
" Description:	Opens the file under the cursor
" Dependency:	cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcNav_OpenFile()
	execute('cs find f '.expand("<cfile>"))
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcNav_SwitchBetweenHeaderImpl()
" Description:	Switches between header and implementation files
" Dependency:	'A' plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcNav_SwitchBetweenHeaderImpl(bShowInVerticalSplit)
	if (a:bShowInVerticalSplit == 1)
		:AV
	else
		:A
	endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcNav_GoToDefinition()
" Description:	Go to definition of token under the cursor
" Dependency:	ctags exuberant
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcNav_GoToDefinition()
	execute('tjump '.expand("<cword>"))
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcNav_FindAllReferences()
" Description:	Find all references to the token under the cursor
" Dependency:	cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcNav_FindAllReferences()
	execute('cs find s '.expand("<cword>"))
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcNav_FindGlobalDefinitions()
" Description:	Find global definitions of token under the cursor
" Dependency:	cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcNav_FindGlobalDefinitions()
	execute('cs find g '.expand("<cword>"))
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcNav_FindAllCallers()
" Description:	Find all functions calling the function under the cursor
" Dependency:	cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcNav_FindAllCallers()
	execute('cs find c '.expand("<cword>"))
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcNav_FindAllCallees()
" Description:	Find all functions called by the function under the cursor
" Dependency:	cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcNav_FindAllCallees()
	execute('cs find d '.expand("<cword>"))
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcNav_FindAllIncludes()
" Description:	Find all files that include the filename under the cursor
" Dependency:	cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcNav_FindAllIncludes()
	execute('cs find i '.expand("<cfile>"))
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcNav_FindAllInstancesOfText()
" Description:	Run 'egrep'of token under the cursor
" Dependency:	cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcNav_FindAllInstancesOfText()
	execute('cs find t '.expand("<cword>"))
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcNav_EGrepSearch()
" Description:	Search for the word under the cursor using 'egrep'
" Dependency:	cscope, egrep
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcNav_EGrepSearch()
	execute('cs find e '.expand("<cword>"))
endfunction


" --------------------------------------------------------------------------------------------------------------------------------------
"
"	SOURCE CODE PARSER API
" 
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcParser_GenerateCxxTags()
" Description:	Starts generation of ctags for C & C++ files in current project
" Dependency:	ctags-exuberant
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcParser_GenerateCxxTags()
	exec ':!ctags -R --languages=C,C++ --c++-kinds=+p --fields=+iaS --extra=+q -f ' . g:project_cxx_tags . ' ' . g:project_full_path
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcParser_GenerateJavaTags()
" Description:	Starts generation of ctags for Java files in current project
" Dependency:	ctags-exuberant
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcParser_GenerateJavaTags()
	exec ':!ctags -R --languages=Java --extra=+q -f ' . g:project_java_tags . ' ' . g:project_full_path
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcParser_GenerateCScope(bRunUpdate)
" Description:	Starts generation of cscope in current project
" Dependency:	cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcParser_GenerateCScope(bRunUpdate)
	exec ':!find ' . g:project_full_path . ' -iname "*.c" -o -iname "*.cpp" -o -iname "*.h" -o -iname "*.hpp" -o -iname "*.java" > ' . g:project_full_path . '/' . 'cscope.files'
	let cmd = ':!cscope -q -R -b -i ' . g:project_full_path . '/' . 'cscope.files'
	if (a:bRunUpdate == 1)
		let cmd .= ' -U'
	endif
	exec cmd
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcParser_UpdateCxxTags()
" Description:	Updates tags for C & C++ files in current project
" Dependency:	ctags-exuberant
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcParser_UpdateCxxTags()
  	let file = expand("%:p")
  	let cmd = 'sed -i ' . '"' . '\:' . file . ':d' . '" ' . g:project_cxx_tags
  	let resp = system(cmd)
  	let cmd = 'ctags --languages=C,C++ --c++-kinds=+p --fields=+iaS --extra=+q -a -f ' . g:project_cxx_tags . ' "' . file . '"'
  	let resp = system(cmd)
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcParser_UpdateJavaTags()
" Description:	Updates tags for Java files in current project
" Dependency:	ctags-exuberant
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcParser_UpdateJavaTags()
  	let file = expand("%:p")
  	let cmd = 'sed -i ' . '"' . '\:' . file . ':d' . '" ' . g:project_java_tags
  	let resp = system(cmd)
  	let cmd = 'ctags --languages=Java --extra=+q -a -f ' . g:project_java_tags . ' "' . file . '"'
  	let resp = system(cmd)
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_SrcParser_UpdateCScope()
" Description:	Updates cscope database in current project
" Dependency:	cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcParser_UpdateCScope()
	call Y_SrcParser_GenerateCScope(1)
	exec 'cscope reset'
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_CScope_Init()
" Description:	Initialization of cscope
" Dependency:	cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_CScope_Init()
	set cscopetag
	set csto=0
	if filereadable(g:project_full_path . '/' . g:project_cscope_db_filename)
		set nocscopeverbose
		execute('cs add ' . g:project_full_path . '/' . g:project_cscope_db_filename)
	endif
	set cscopeverbose
endfunction

" --------------------------------------------------------------------------------------------------------------------------------------
"
"	STATIC ANALYSIS API
" 
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_Analyzer_RunCppCheck()
" Description:	Runs the 'cppcheck' on given path
" Dependency:	cppcheck
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Analyzer_RunCppCheck(path, ...)
	let additional_args = ''
	if a:0 != 0
		let additional_args = a:1
		let i = 2
		while i <= a:0
		    execute "let additional_args = additional_args . \" \" . a:" . i
		    let i = i + 1
		endwhile
    endif

    let mp = &makeprg
    let &makeprg = 'cppcheck --enable=all --force --quiet --template=gcc ' . additional_args . ' ' . a:path
	exec "make!"
    let &makeprg = mp
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_Analyzer_RunClangChecker()
" Description:	Runs the 'clang' static analysis on given path
" Dependency:	clang
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Analyzer_RunClangChecker(path, ...)
	let analysis = '-analyzer-store=region -analyzer-opt-analyze-nested-blocks -analyzer-eagerly-assume -analyzer-checker=core -analyzer-checker=unix -analyzer-checker=deadcode -analyzer-checker=cplusplus -analyzer-checker=security.insecureAPI.UncheckedReturn -analyzer-checker=security.insecureAPI.getpw -analyzer-checker=security.insecureAPI.gets -analyzer-checker=security.insecureAPI.mktemp -analyzer-checker=security.insecureAPI.mkstemp -analyzer-checker=security.insecureAPI.vfork -analyzer-output plist'
	let mp = &makeprg
	let &makeprg = 'clang++ -cc1 -analyze -triple arm-none-linux-eabi ' . analysis
	exec "make!"
	let makeprg = &mp
endfunction


" --------------------------------------------------------------------------------------------------------------------------------------
"
"	BUILD MANAGEMENT API
" 
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_Build_RunMake()
" Description:	Run the build via Makefile. 
" 				When finished, open the quickfix window and avoid jumping to the first error.
" 				Warnings are currently treated as errors so this feature can easily start to become annoying.
" Dependency:	GNU make
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Build_RunMake(...)
	let additional_args = ''
	if a:0 != 0
		let additional_args = a:1
		let i = 2
		while i <= a:0
		    execute "let additional_args = additional_args . \" \" . a:" . i
		    let i = i + 1
		endwhile
    endif
    
	let mp = &makeprg
    let &makeprg = 'make ' . additional_args
	exec "make! | copen"
    let &makeprg = mp
endfunction


" --------------------------------------------------------------------------------------------------------------------------------------
"
"	LAYOUT MANAGEMENT API
" 
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	Y_Layout_Refresh()
" Description:	Setups the default layout
" Dependency:	NERDTree, Tagbar
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_Layout_Refresh()
	execute('NERDTree ' . g:project_full_path)
	execute('TagbarOpen')
	call setqflist([])
	execute('copen')
endfunction

