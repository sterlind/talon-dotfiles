app: vscode
-
tag(): user.tabs
tag(): user.git

action(app.tab_close): user.vscode("workbench.action.closeActiveEditor")
action(app.tab_next): user.vscode("workbench.action.nextEditorInGroup")
action(app.tab_previous): user.vscode("workbench.action.previousEditorInGroup")
action(app.tab_reopen): user.vscode("workbench.action.reopenClosedEditor")
action(app.window_close): user.vscode("workbench.action.closeWindow")
action(app.window_open): user.vscode("workbench.action.newWindow")

^git commit$: user.vscode("git.commitStaged")
^git status$: user.vscode("workbench.scm.focus")
^git pull$: user.vscode("git.pullRebase")

# Sidebar
bar (show | hide):               user.vscode("workbench.action.toggleSidebarVisibility")
bar explore:                     user.vscode("workbench.view.explorer")
bar extensions:                  user.vscode("workbench.view.extensions")
bar outline:                     user.vscode("outline.focus")
bar debug:                       user.vscode("workbench.view.debug")
bar search:                      user.vscode("workbench.view.search")
bar source:                      user.vscode("workbench.view.scm")
bar file:                        user.vscode("workbench.files.action.showActiveFileInExplorer")

ref last:                        user.vscode("references-view.prev")
ref next:                        user.vscode("references-view.next")

hunt all: user.vscode("workbench.action.findInFiles")
result next: key(f4)
result previous: key(shift-f4)
results collapse: user.vscode("workbench.files.action.collapseExplorerFolders")

next:                            user.vscode("jumpToNextSnippetPlaceholder")

nope: key(ctrl-z)
redo: key(ctrl-y)

# File commands
file hunt [<user.text>]:
    user.vscode("workbench.action.quickOpen")
    sleep(50ms)
    insert(text or "")
file create sibling: user.vscode("explorer.newFile")
file rename:
    user.vscode("fileutils.renameFile")
    sleep(150ms)
file move:
	  user.vscode("fileutils.moveFile")
	  sleep(150ms)
folder new: user.vscode("explorer.newFolder")
file new: user.vscode("explorer.newFile")
file open folder: user.vscode("revealFileInOS")
file reveal: user.vscode("workbench.files.action.showActiveFileInExplorer")
save: user.vscode("workbench.action.files.saveWithoutFormatting")

# Search commands
scout symbol [<user.text>] [over]:
    user.vscode("workbench.action.gotoSymbol")
    sleep(50ms)
    insert(text or "")

pop symbol <user.text> [over]:
    user.vscode("workbench.action.gotoSymbol")
    sleep(50ms)
    insert(text or "")
    sleep(250ms)
    key(enter)
    sleep(50ms)

scout all symbol [<user.text>] [halt]:
    user.vscode("workbench.action.showAllSymbols")
    sleep(50ms)
    insert(text or "")

pop all symbol <user.text> [halt]:
    user.vscode("workbench.action.showAllSymbols")
    sleep(50ms)
    insert(text or "")
    sleep(250ms)
    key(enter)
    sleep(50ms)