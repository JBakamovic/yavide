" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Project management
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap        <C-s>n              :YavideProjectNew<CR>|"                                         New project
nmap        <C-s>o              :YavideProjectOpen<CR>|"                                        Open project
nmap        <C-s>i              :YavideProjectImport<CR>|"                                      Import project
nmap        <C-s>c              :YavideProjectClose<CR>|"                                       Close project
nmap        <C-s>s              :YavideProjectSave<CR>|"                                        Save project
nmap        <C-s>d              :YavideProjectDelete<CR>|"                                      Delete project

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Search tools
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
noremap     <C-f>               :YavidePromptFind<CR>|"                                         Open find dialog
vnoremap    <C-f>               :YavidePromptFind<CR>
onoremap    <C-f>               <C-C>:YavidePromptFind<CR>
inoremap    <C-f>               <C-O>:YavidePromptFind<CR>
cnoremap    <C-f>               <C-C>:YavidePromptFind<CR>
noremap     <C-f>               :YavidePromptFindAndReplace<CR>|"                               Open find and replace dialog
vnoremap    <C-f>               :YavidePromptFindAndReplace<CR>
onoremap    <C-f>               <C-C>:YavidePromptFindAndReplace<CR>
inoremap    <C-f>               <C-O>:YavidePromptFindAndReplace<CR>
cnoremap    <C-f>               <C-C>:YavidePromptFindAndReplace<CR>

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Buffer management
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap        <C-s>               <ESC>:YavideBufferSave<CR>|"                                    Save current buffer (normal mode)
imap        <C-s>               <ESC>:YavideBufferSave<CR>i|"                                   Save current buffer (insert mode)
nnoremap    <C-c>               :YavideBufferClose<CR>|"                                        Close current buffer
nnoremap    <C-M-c>             :YavideBufferCloseAllButCurrentOne<CR>|"                        Close all buffers but the current one
nnoremap    <C-c>a              :YavideBufferCloseAll<CR>|"                                     Close all buffers
map         <C-s-Tab>           :YavideBufferPrev<CR>|"                                         Go to previous buffer
map         <C-Tab>             :YavideBufferNext<CR>|"                                         Go to next buffer
nnoremap    <C-Down>            :YavideBufferScrollDown<CR>|"                                   Scroll buffer by one line (down)
nnoremap    <C-Up>              :YavideBufferScrollUp<CR>|"                                     Scroll buffer by one line (up)

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Buffer editing
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nnoremap    <C-a>               ggVG|"                                                          Select all
vnoremap    <C-x>               "+x|"                                                           Cut
vnoremap    <C-c>               "+y|"                                                           Copy
map         <C-v>               "+gP|"                                                          Paste (with some black magic from https://github.com/vim/vim/blob/master/runtime/mswin.vim)
cmap        <C-v>               <C-R>+
exe         'inoremap <script>  <C-v> <C-G>u' . paste#paste_cmd['i']
exe         'vnoremap <script>  <C-v> '       . paste#paste_cmd['v']
nnoremap    <C-z>               u|"                                                             Undo
inoremap    <C-z>               <C-O>u
noremap     <C-R>               <C-R>|"                                                         Redo
inoremap    <C-R>               <C-O><C-R>
nnoremap    <CR>                :let @/ = ""<CR><CR>|"                                          Clear highlighted text occurences
nnoremap    <Tab>               >>|"                                                            Configure indent mechanism to act as in other editors
nnoremap    <S-Tab>             <<
inoremap    <S-Tab>             <C-D>
vnoremap    <Tab>               >gv
vnoremap    <S-Tab>             <gv

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Source code navigation
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap        <F3>                :YavideSrcNavOpenFile<CR>|"                                     Open file under the cursor
imap        <F3>                <ESC>:YavideSrcNavOpenFile<CR>i|"
nmap        <F4>                :YavideSrcNavSwitchBetweenHeaderImpl<CR>|"                      Switch between header/source
imap        <F4>                <ESC>YavideSrcNavSwitchBetweenHeaderImpl<CR>i|"
nmap        <S-F4>              :YavideSrcNavSwitchBetweenHeaderImplVSplit<CR>|"                Switch between header/source in a vertical split
imap        <S-F4>              <ESC>:YavideSrcNavSwitchBetweenHeaderImplVSplit<CR>i|"
nmap        <F12>               :YavideSrcNavGoToDefinition<CR>|"                               Goto definition
imap        <F12>               :YavideSrcNavGoToDefinition<CR>|"
nmap        <C-LeftMouse>       :YavideSrcNavGoToDefinition<CR>|"
imap        <C-LeftMouse>       :YavideSrcNavGoToDefinition<CR>|"
nmap        <S-F12>             :vsp <CR>:YavideSrcNavGoToDefinition<CR>|"                      Goto definition in a vertical split
imap        <S-F12>             :vsp <CR>:YavideSrcNavGoToDefinition<CR>|"
nmap        <C-\>s              :YavideSrcNavFindAllReferences<CR>|"                            Find all references to the token under the cursor
nmap        <C-\>r              :YavideSrcNavRebuildIndex<CR>|"                                 Rebuild symbol database index for current project
nnoremap    <M-Left>            <C-O>"                                                          Jump back to previous cursor location
nnoremap    <M-Right>           <C-I>"                                                          Jump to next cursor location

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Build process
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap        <F7>                :YavideBuildRun<CR>|"                                           Build project
imap        <F7>                <ESC>:w<CR>:YavideBuildRun<CR>|"
