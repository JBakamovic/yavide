# Contents
* [Usage](#usage-overview)

# Usage overview

Category                          | Shortcut                          | Description
--------------------------------- | --------------------------------- | ---------------------------------
|**Project management**            |                                   |
|                                  | `<Ctrl-s>n`                       | Create new project
|                                  | `<Ctrl-s>i`                       | Import project with already existing code base
|                                  | `<Ctrl-s>o`                       | Open project
|                                  | `<Ctrl-s>c`                       | Close project
|                                  | `<Ctrl-s>s`                       | Save project
|                                  | `<Ctrl-s>d`                       | Delete project
|**Buffer management**             |                                   |
|                                  | `<Ctrl-c>`                        | Close current buffer
|                                  | `<Ctrl-c-a>`                      | Close all buffers
|                                  | `<Ctrl-Alt-c>`                    | Close all buffers but the current one
|                                  | `<Ctrl-s>`                        | Save current buffer
|                                  | `<Ctrl-Tab>`                      | Go to next buffer
|                                  | `<Ctrl-Shift-Tab>`                | Go to previous buffer
|                                  | `<Ctrl-Down>`                     | Scroll buffer by one line (down)
|                                  | `<Ctrl-Up>`                       | Scroll buffer by one line (up)
|**Buffer modes**                  |                                   |
|                                  | `<ESC>`                           | Enter the `normal` mode
|                                  | `<a>`                             | Enter the `insert` mode (append after cursor)
|                                  | `<i>`                             | Enter the `insert` mode (insert before cursor)
|                                  | `<Shift-v>`                       | Enter the `visual` mode (line mode)
|                                  | `<v>`                             | Enter the `visual` mode (character mode)
|**Buffer editing**                |                                   |
|                                  | `<Ctrl-a>`                        | Select all
|                                  | `<Ctrl-x>`                        | Cut
|                                  | `<Ctrl-c>`                        | Copy
|                                  | `<Ctrl-v>`                        | Paste
|                                  | `<Ctrl-z>`                        | Undo
|                                  | `<Ctrl-r>`                        | Redo
|                                  | `<Shift-s>`                       | Delete the whole line
|                                  | `<*>` or `<Shift-LeftMouse>`      | Highlight all occurrences of text under the cursor
|                                  | `<Enter>`                         | Clear highlighted text occurences
|                                  | `<Ctrl-n>`                        | Start multiple-selection editing with the text under the cursor. Each consecutive press will highlight the next occurrence of selected text. After all occurrences have been marked, do the text editing with usual commands (`c`, `s`, `i`, `a`, etc.).
|                                  | `<Ctrl-p>`                        | When in multiple-selection editing mode, one may press this key combination to remove the current occurrence and go back to the previous one.
|                                  | `<Ctrl-x>`                        | When in multiple-selection editing mode, one may press this key combination to skip the current occurrence and go to the following one.
|**Window management**             |                                   |
|                                  | `<Ctrl-w>c`                       | Close current window
|                                  | `<Ctrl-w><Arrow>`                 | Navigate through windows using `<left>`, `<right>`, `<up>` & `<down>` arrows
|                                  | `<Ctrl-w>s`                       | Create new horizontal window split
|                                  | `<Ctrl-w>v`                       | Create new vertical window split
|                                  | `<Ctrl-w>=`                       | Make split windows equal in size
|**Search utilities**              |                                   |
|                                  | `<Ctrl-f>`                        | Open search dialog
|                                  | `<Ctrl-h>`                        | Open search and replace dialog
|                                  | `:grep <input>`                   | Run `grep` with provided `<input>`
|**Source code commenting**        |                                   |
|                                  | `<,cA>`                           | Insert comment at the current line
|                                  | `<,cc>`                           | Comment the selected line/block
|                                  | `<,cs>`                           | Comment the selected line/block (other style)
|                                  | `<,cu>`                           | Uncomment the selected line/block
|**Source code navigation**        |                                   |
|                                  | `<F3>`                            | Open file under the cursor
|                                  | `<F4>`                            | Switch between header & corresponding implementation file
|                                  | `<Shift-F4>`                      | Switch between header & implementation (in a vertical split window)
|                                  | `<F12>` or `<Ctrl-LeftMouse>`     | Goto definition of token under the cursor
|                                  | `<Shift-F12>`                     | Goto definition of token under the cursor (in a vertical split window)
|                                  | `<Ctrl-t>` or `<Ctrl-RightMouse>` | Jump back from definition
|                                  | `<Ctrl-\>s`                       | Find all references to token under the cursor
|                                  | `<Ctrl-\>g`                       | Find global definition(s) of token under the cursor
|                                  | `<Ctrl-\>c`                       | Find all functions calling the function under the cursor
|                                  | `<Ctrl-\>d`                       | Find all functions called by the function under the cursor
|                                  | `<Ctrl-\>i`                       | Find all files that include the filename under the cursor
|                                  | `<Ctrl-\>t`                       | Find all instances of the text under the cursor
|                                  | `<Ctrl-\>e`                       | Search for the word under the cursor using `egrep`
|**Source code static analysis**   |                                   |
|                                  | `:YavideAnalyzerCppCheckBuf`      | Runs the `cppcheck` static analysis on current buffer
|                                  | `:YavideAnalyzerCppCheck`         | Runs the `cppcheck` static analysis on whole project
|**Build management**              |                                   |
|                                  | `<F7>`                            | Build project.
|**SCM Git client**                |                                   |
|                                  | `:Gstatus`                        | Runs `git status`
|                                  | `:Gcommit`                        | Runs `git commit`
|                                  | `:Gmerge`                         | Runs `git merge`
|                                  | `:Gpull`                          | Runs `git pull`
|                                  | `:Gpush`                          | Runs `git push`
|                                  | `:Gfetch`                         | Runs `git fetch`
|                                  | `:Glog`                           | Runs `git log`
|                                  | `:Gdiff`                          | Runs `git diff`
|                                  | `:Gblame`                         | Runs `git blame`
|**Misc**                          |                                   |
|                                  | `:YavideLayoutRefresh`            | Refresh the layout (opens up project explorer, class browser and clears up the `quickfix` window)
|                                  | `:sh`                             | Enter the `bash` shell


