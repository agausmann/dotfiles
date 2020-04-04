" appearance
syntax enable
set number
set showcmd
set showmatch
set wildmenu
colorscheme base16

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

let g:rustfmt_autosave = 1 " format .rs on save

" custom file types
filetype plugin indent on
autocmd FileType yaml,yml setlocal tabstop=2 softtabstop=2 shiftwidth=2
autocmd FileType markdown,plaintex,rst,tex,text setlocal textwidth=79
