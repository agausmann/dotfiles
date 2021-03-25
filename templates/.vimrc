" appearance
syntax enable
set number
set showcmd
set showmatch
set wildmenu
colorscheme base16
" fix unreadable ALE errors
exec "highlight SpellBad guifg=#".g:base16_gui05." guibg=#".g:base16_gui08." ctermfg=".g:base16_cterm05." ctermbg=".g:base16_cterm08
exec "highlight SpellCap guifg=#".g:base16_gui00." guibg=#".g:base16_gui0D." ctermfg=".g:base16_cterm00." ctermbg=".g:base16_cterm0D

" behavior
noremap j gj
noremap k gk
inoremap jk <esc> 
set hlsearch
set incsearch
set lazyredraw
set directory=~/.vim/tmp

set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab

set autochdir

let g:rustfmt_autosave = 1 " format .rs on save

" custom file types
filetype plugin indent on
autocmd FileType yaml,yml setlocal tabstop=2 softtabstop=2 shiftwidth=2
autocmd FileType markdown,plaintex,rst,tex,text setlocal textwidth=79
autocmd BufNewFile,BufRead *.qml set smartindent filetype=javascript
