" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ServerStart()
" Description:  Starts Yavide server background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ServerStart()
python << EOF
import os
import server.runner
import tempfile
vim_server_name = vim.eval('v:servername')
server.runner.run(
    'Vim',
    server_queue,
    vim_server_name,
    tempfile.gettempdir() + os.sep + vim_server_name + '_server.log'
)
EOF
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ServerStartAllServices()
" Description:  Starts all Yavide server background services.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ServerStartAllServices()
    for service in g:project_available_services
        if service['enabled']
            call service['start']()
        endif
    endfor
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ServerStartService()
" Description:  Starts specific Yavide server background services.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ServerStartService(id, payload)
python << EOF
server_queue.put([0xF1, vim.eval('a:id'), vim.eval('a:payload')])
EOF
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ServerSendServiceRequest()
" Description:  Sends request to particular server background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ServerSendServiceRequest(id, payload)
python << EOF
server_queue.put([0xF2, int(vim.eval('a:id')), vim.eval('a:payload')])
EOF
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ServerStopAllServices()
" Description:  Stops all Yavide server background services.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ServerStopAllServices(subscribe_for_shutdown_callback)
    " Stop background services
    for service in g:project_available_services
        if service['enabled']
            call service['stop'](a:subscribe_for_shutdown_callback)
        endif
    endfor
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ServerStopService()
" Description:  Stops specific Yavide server backround service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ServerStopService(id, subscribe_for_shutdown_callback)
python << EOF
server_queue.put([0xFE, vim.eval('a:id'), vim.eval('a:subscribe_for_shutdown_callback')])
EOF
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ServerStop()
" Description:  Stops Yavide server background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ServerStop()
python << EOF
server_queue.put([0xFF, 0xFF, False])
EOF
endfunction

