"
" ~/.vimrc
" author: adam gausmann
"


" appearance
" =========

set number
set showcmd
set incsearch
set hlsearch

" syntax
filetype plugin on
syntax on


" rebinds
" ==========

noremap ; l
noremap l k
noremap k j
noremap j h
inoremap jk <esc>


" indentation
" ===========

set tabstop=4
set softtabstop=4
set expandtab
filetype indent on
set shiftwidth=4
